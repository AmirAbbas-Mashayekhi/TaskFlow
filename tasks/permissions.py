from rest_framework.permissions import BasePermission
from .models import Participant


class IsRegisteredParticipant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and Participant.objects.filter(user_id=request.user.id).exists()
        )


class IsNotRegisteredParticipant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and not Participant.objects.filter(user_id=request.user.id).exists()
        )
