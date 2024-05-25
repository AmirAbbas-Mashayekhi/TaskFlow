from django.contrib import admin
from .models import Task, Participant, Comment, Project


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'first_name', 'last_name']
    list_select_related = ['user']
    autocomplete_fields = ['user']
    search_fields = ['user_name__istartswith']
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
    search_fields = ['title__istartswith']
    autocomplete_fields = ['assignees', 'project']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'posted_at', 'task']
    autocomplete_fields = ['user', 'task']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'start_date', 'end_date']
    list_select_related = ['owner__user']
    autocomplete_fields = ['owner']
    search_fields = ['title__istartswith']
