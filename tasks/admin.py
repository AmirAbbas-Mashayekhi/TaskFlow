from django.contrib import admin

from .models import Task, Participant, Comment, Project, Team


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'first_name', 'last_name']
    list_select_related = ['user']
    autocomplete_fields = ['user']
    search_fields = ['user__username__istartswith']
    list_per_page = 10


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'project',
        'priority',
        'status',
        'created_at',
        'due_date',
        'expected_duration'
    ]
    list_editable = ['priority', 'status']
    list_per_page = 20
    search_fields = ['title']
    autocomplete_fields = ['assignees', 'project']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'members_count']
    search_fields = ['title']
    autocomplete_fields = ['members', 'leader']
    list_per_page = 10

    @staticmethod
    def members_count(team):
        return team.members.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'posted_at', 'task']
    autocomplete_fields = ['user', 'task']
    list_per_page = 10


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'team', 'start_date', 'end_date']
    autocomplete_fields = ['team']
    search_fields = ['title__istartswith']
    list_per_page = 10
