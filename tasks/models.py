import uuid
from datetime import datetime
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Participant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneNumberField()


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(Participant, on_delete=models.CASCADE)


class Task(models.Model):
    PRIORITY_CRITICAL = 'C'
    PRIORITY_HIGH = 'H'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_LOW = 'L'
    PRIORITY_CHOICES = [
        (PRIORITY_CRITICAL, 'Critical'),
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_LOW, 'Low')
    ]

    STATUS_BACKLOG = 'B'
    STATUS_TODO = 'T'
    STATUS_DOING = 'D'
    STATUS_FINISHED = 'F'
    STATUS_ARCHIVED = 'A'
    STATUS_CHOICES = [
        (STATUS_BACKLOG, 'Backlog'),
        (STATUS_TODO, 'Todo'),
        (STATUS_DOING, 'Doing'),
        (STATUS_FINISHED, 'Finished'),
        (STATUS_ARCHIVED, 'Archived')
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignees = models.ManyToManyField(Participant, related_name='assignees')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_BACKLOG)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    expected_duration = models.PositiveSmallIntegerField()


class Comment(models.Model):
    user = models.ForeignKey(Participant, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
