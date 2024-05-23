from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Participant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = PhoneNumberField()
