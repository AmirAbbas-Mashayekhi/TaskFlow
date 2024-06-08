from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Invitation, Participant, Project, Role, Team, TeamMember


class ParticipantSerializer(ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Participant
        fields = ["id", "user_id", "phone"]

    def create(self, validated_data):
        participant = Participant(**validated_data, user_id=self.context["user_id"])
        participant.save()
        return participant


class TeamMemberSerializer(ModelSerializer):

    class Meta:
        model = TeamMember
        fields = ["id", "participant", "joined"]


class TeamSerializer(ModelSerializer):
    members = TeamMemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ["id", "title", "leader", "members"]


class CreateTeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "title"]

    def create(self, validated_data):
        leader = Participant.objects.get(user_id=self.context["user_id"])
        team = Team(**validated_data, leader=leader)
        team.save()
        return team


class InvitationSerializer(ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["id", "email", "team", "accepted", "created_at"]


class CreateInvitationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        participant = Participant.objects.filter(user__email=value)

        if not participant.exists():
            raise serializers.ValidationError("User with this email does not exist.")
        if TeamMember.objects.filter(
            team=self.context["team"], participant_id=participant.first().id
        ).exists():
            raise serializers.ValidationError("User Already Added to the Team.")
        if Invitation.objects.filter(team=self.context["team"], email=value).exists():
            raise serializers.ValidationError("Invitation Already sent.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        team = self.context["team"]
        invitation = Invitation(email=email, team=team)
        invitation.save()
        return invitation


class ProjectSerializer(ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "team",
        ]


class CreateProjectSerializer(ModelSerializer):
    team_id = serializers.IntegerField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "team_id",
        ]

    def validate_team_id(self, value: int):
        participant = Participant.objects.get(user_id=self.context["user_id"])

        if not Team.objects.filter(pk=value, leader=participant).exists():
            raise serializers.ValidationError("Team does not exist.")
        return value


class UpdateProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
        ]


class RoleSerializer(ModelSerializer):
    project_id = serializers.IntegerField()
    participant_id = serializers.IntegerField()

    class Meta:
        model = Role
        fields = [
            "id",
            "title",
            "project_id",
            "participant_id",
        ]

    def validate_project_id(self, value):
        current_participant = Participant.objects.get(user_id=self.context["user_id"])

        if not Project.objects.filter(
            pk=value,
            team__leader=current_participant,
        ).exists():
            raise serializers.ValidationError(
                "No project/participant matches the criteria."
            )
        return value

    def validate_participant_id(self, value):
        if not TeamMember.objects.filter(participant_id=value).exists():
            raise serializers.ValidationError(
                "No project/participant matches the criteria."
            )
        return value
