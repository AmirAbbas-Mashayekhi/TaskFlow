from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Participant


class ParticipantSerializer(ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'user_id', 'phone']

    def create(self, validated_data):
        participant = Participant(**validated_data, user_id=self.context['user_id'])
        participant.save()
        return participant
