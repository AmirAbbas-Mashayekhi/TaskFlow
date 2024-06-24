from datetime import datetime
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.permissions import IsNotRegisteredParticipant, IsRegisteredParticipant
from tasks.tasks import send_invitation_email
from .models import (
    Assignee,
    Invitation,
    Participant,
    Project,
    Role,
    Task,
    Team,
    TeamMember,
)
from .serializers import (
    AssigneeSerializer,
    CreateInvitationSerializer,
    CreateProjectSerializer,
    CreateTeamSerializer,
    InvitationSerializer,
    ParticipantSerializer,
    ProjectSerializer,
    RoleSerializer,
    TaskSerializer,
    TeamMemberSerializer,
    TeamSerializer,
    UpdateProjectSerializer,
)


class ParticipantViewSet(ModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAdminUser]
    queryset = Participant.objects.all()

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    @action(
        methods=["GET", "PUT"],
        permission_classes=[IsRegisteredParticipant],
        detail=False,
    )
    def me(self, request):
        participant = Participant.objects.get(user_id=request.user.id)
        if self.request.method == "PUT":
            serializer = ParticipantSerializer(participant, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        if self.request.method == "GET":
            serializer = ParticipantSerializer(participant)
            return Response(serializer.data)

    @action(
        methods=["POST"],
        permission_classes=[IsAuthenticated, IsNotRegisteredParticipant],
        detail=False,
    )
    def register(self, request):
        if Participant.objects.filter(user_id=request.user.id).exists():
            return Response({"message": "You are already registered."})
        serializer = ParticipantSerializer(
            data=request.data, context={"user_id": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Team.objects.all()
        return Team.objects.filter(leader__user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "invite":
            return CreateInvitationSerializer
        if self.request.method in ["POST", "PUT"]:
            return CreateTeamSerializer
        return TeamSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Participant.DoesNotExist:
            return Response(
                {"error": "Participant Does Not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["POST"])
    def invite(self, request, pk=None):
        team = self.get_object()
        serializer = CreateInvitationSerializer(
            data=request.data, context={"team": team}
        )
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        acceptance_link = self.build_acceptance_link(request, invitation.token)
        self.send_invitation_email(invitation, team.title, acceptance_link)

        return Response({"message": "Invitation Sent."})

    def build_acceptance_link(self, request, token):
        relative_link = reverse("invitation-accept", args=[token])
        return request.build_absolute_uri(relative_link)

    def send_invitation_email(self, invitation, team_name, acceptance_link):
        send_invitation_email.delay(invitation.email, team_name, acceptance_link)


class TeamMemberViewSet(ModelViewSet):
    serializer_class = TeamMemberSerializer
    http_method_names = ["get", "delete", "options", "head"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamMember.objects.filter(team_id=self.kwargs["teams_pk"])

    def destroy(self, request, *args, **kwargs):
        team_member: TeamMember = self.get_object()
        invitation = Invitation.objects.get(
            team_id=self.kwargs["teams_pk"], email=team_member.participant.user.email
        )
        invitation.delete()
        team_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = InvitationSerializer
    http_method_names = ["head", "options", "get", "delete"]

    @action(
        detail=False,
        methods=["GET"],
        url_path="accept/(?P<token>[^/.]+)",
        name="invitation-accept",
        permission_classes=[AllowAny],
    )
    def accept_invitation(self, request, token=None):
        invitation = Invitation.objects.filter(token=token, accepted=False).first()

        if not invitation:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participant = Participant.objects.get(user__email=invitation.email)
        TeamMember.objects.create(team=invitation.team, participant=participant)
        invitation.accepted = True
        invitation.save()

        return Response(
            {"message": "Invitation accepted and user added to the team."},
            status=status.HTTP_200_OK,
        )


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsRegisteredParticipant]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()

        participant = Participant.objects.get(user_id=self.request.user.id)
        return Project.objects.select_related("team").filter(team__leader=participant)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateProjectSerializer
        if self.request.method == "PUT":
            return UpdateProjectSerializer
        return ProjectSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    @action(detail=False, methods=["GET"])
    def active_projects(self, request):
        participant = Participant.objects.get(user_id=request.user.id)
        projects = Project.objects.select_related("team").filter(
            team__leader=participant, end_date__gt=datetime.now()
        )
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class RoleViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [IsRegisteredParticipant]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Role.objects.all()
        participant = Participant.objects.get(user_id=self.request.user.id)
        return Role.objects.filter(project__team__leader=participant)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsRegisteredParticipant]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        participant_id = Participant.objects.values("id").get(user_id=user.id)
        return Task.objects.filter(project__team__leader_id=participant_id["id"])

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class AssigneeViewSet(ModelViewSet):
    http_method_names = ["head", "options", "get", "post", "delete"]

    def get_queryset(self):
        return Assignee.objects.filter(task_id=self.kwargs["tasks_pk"])

    def get_serializer_class(self):
        return AssigneeSerializer

    def get_serializer_context(self):
        return {"task_id": self.kwargs["tasks_pk"]}
