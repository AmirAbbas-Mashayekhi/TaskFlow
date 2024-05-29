from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Participant
from .serializers import ParticipantSerializer


class ParticipantViewSet(ModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAdminUser]
    queryset = Participant.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"error": 'User Already has an associated participant.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['GET', 'PUT'], permission_classes=[IsAuthenticated], detail=False)
    def me(self, request):
        participant = Participant.objects.get(user_id=self.request.user.id)
        if self.request.method == 'PUT':
            serializer = ParticipantSerializer(participant, data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        if self.request.method == 'GET':
            serializer = ParticipantSerializer(participant)
            return Response(serializer.data)

# TODO: Create TeamViewSet
