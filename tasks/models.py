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
