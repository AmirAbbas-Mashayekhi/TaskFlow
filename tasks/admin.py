from django.contrib import admin
from .models import (
    Invitation,
    Task,
    Participant,
    Comment,
    Project,
    Team,
    Role,
    TeamMember,
)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["id", "user_name", "first_name", "last_name"]
    list_select_related = ["user"]
    autocomplete_fields = ["user"]
    search_fields = ["user__username__istartswith"]
    list_per_page = 10


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "project",
        "priority",
        "status",
        "created_at",
        "due_date",
        "expected_duration",
    ]
    list_editable = ["priority", "status"]
    list_per_page = 20
    search_fields = ["title"]
    autocomplete_fields = ["assignees", "project"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["title", "leader", "members_count"]
    search_fields = ["title"]
    autocomplete_fields = ["leader"]
    list_per_page = 10

    @staticmethod
    def members_count(team):
        return team.members.count()


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["id", "team", "participant", "joined"]
    autocomplete_fields = ["team", "participant"]
    list_select_related = ["participant__user"]
    list_per_page = 10


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ["email", "team", "accepted", "created_at"]
    autocomplete_fields = ["team"]
    list_editable = ["accepted"]
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "posted_at", "task"]
    autocomplete_fields = ["user", "task"]
    list_per_page = 10


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "team", "start_date", "end_date"]
    autocomplete_fields = ["team"]
    search_fields = ["title__istartswith"]
    list_per_page = 10


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "participant"]
    autocomplete_fields = ["project"]
    search_fields = ["title__istartswith"]
    list_per_page = 10
