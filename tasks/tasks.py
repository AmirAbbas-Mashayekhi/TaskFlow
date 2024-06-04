from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError
from rest_framework.response import Response
from celery import shared_task
from templated_mail.mail import BaseEmailMessage


@shared_task
def send_invitation_email(email, team_name, acceptance_link):
    try:
        message = BaseEmailMessage(
            template_name="tasks/emails/invitation.html",
            context={"team_name": team_name, "acceptance_link": acceptance_link},
        )
        message.send([email])
    except BadHeaderError:
        return Response({"error": "bad Header Error."})
