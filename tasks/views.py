from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.permissions import IsNotRegisteredParticipant, IsRegisteredParticipant
from tasks.tasks import send_invitation_email
from .models import Invitation, Participant, Team, TeamMember
from .serializers import (
    CreateInvitationSerializer,
    CreateTeamSerializer,
    InvitationSerializer,
    ParticipantSerializer,
    TeamMemberSerializer,
    TeamSerializer,
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
        permission_classes=[AllowAny]
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
