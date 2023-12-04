#views.py
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event, Invitation
from .serializers import UserSerializer, EventSerializer, InvitationSerializer, UserLoginSerializer

class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class CreateEvent(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        return Response({'message': 'Event created successfully'}, status=status.HTTP_200_OK)

class UpdateEvent(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        event = self.get_object()
        if self.request.user != event.creator:
            raise PermissionDenied("You do not have permission to edit this event.")
        serializer.save()
        return Response({'message': 'Event updated successfully'}, status=status.HTTP_200_OK)


class DeleteEvent(generics.DestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user != instance.creator:
            raise PermissionDenied("You do not have permission to delete this event.")
        instance.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_200_OK)

class InviteToEvent(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.request.data.get('event_id')
        invitee_id = self.request.data.get('invitee')
        event = get_object_or_404(Event, id=event_id)
        invitee = get_object_or_404(User, id=invitee_id)
        if self.request.user != event.creator:
            raise PermissionDenied("You do not have permission to invite users to this event.")
        serializer.save(event=event, invitee=invitee)
        return Response({'message': 'User invited successfully'}, status=status.HTTP_200_OK)

class ViewCreatedEvents(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)


class ViewEventUserInvitedTo(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        invitations = Invitation.objects.filter(invitee=self.request.user)
        event_ids = invitations.values_list('event', flat=True)
        events = Event.objects.filter(id__in=event_ids)
        return events


class ViewUsersInvitedToEvent(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id)

        if self.request.user != event.creator:
            raise PermissionDenied("You do not have permission to view invitees of this event.")
        invitations = Invitation.objects.filter(event_id=event_id)
        invited_users = [invitation.invitee for invitation in invitations]
        
        return invited_users


