import uuid
from datetime import datetime
from django.conf import settings
from django.contrib import admin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Participant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneNumberField(unique=True)

    # TODO:
    #      problematic in automatic user profile creation after authentication

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    @admin.display(ordering="user__username")
    def user_name(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["user__username"]


class Team(models.Model):
    title = models.CharField(max_length=255)
    leader = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.participant.user_name()

    class Meta:
        unique_together = [['team', 'participant']]

class Invitation(models.Model):
    email = models.EmailField(max_length=254)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation to {self.email} for team {self.team}"


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Role(models.Model):
    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["participant", "project"]]


class Task(models.Model):
    PRIORITY_CRITICAL = "C"
    PRIORITY_HIGH = "H"
    PRIORITY_MEDIUM = "M"
    PRIORITY_LOW = "L"
    PRIORITY_CHOICES = [
        (PRIORITY_CRITICAL, "Critical"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_LOW, "Low"),
    ]

    STATUS_BACKLOG = "B"
    STATUS_TODO = "T"
    STATUS_DOING = "D"
    STATUS_FINISHED = "F"
    STATUS_ARCHIVED = "A"
    STATUS_CHOICES = [
        (STATUS_BACKLOG, "Backlog"),
        (STATUS_TODO, "Todo"),
        (STATUS_DOING, "Doing"),
        (STATUS_FINISHED, "Finished"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Participant, blank=True)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_LOW
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_BACKLOG
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    expected_duration = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(Participant, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} comment"
