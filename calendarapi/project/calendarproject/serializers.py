#serializers.py

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event, Invitation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'date', 'creator', 'participants')

    def create(self, validated_data):
        participants_data = validated_data.pop('participants', [])
        event = Event.objects.create(**validated_data)
        if participants_data:
            for participant_data in participants_data:
                user = User.objects.get(pk=participant_data['id'])
                event.participants.add(user)
        return event

class InvitationSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='event.id')
    invitee_id = serializers.ReadOnlyField(source='invitee.id')

    class Meta:
        model = Invitation
        fields = ('id', 'event_id', 'invitee_id')
