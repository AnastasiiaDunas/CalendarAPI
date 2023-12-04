from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .serializers import UserSerializer, EventSerializer, InvitationSerializer
from .models import Event, Invitation

class ModelTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.event = Event.objects.create(title='Sample Event', description='Sample Description', date='2023-12-31 00:00', creator=self.user)

    def test_create_event(self):
        self.assertEqual(self.event.title, 'Sample Event')
        self.assertEqual(self.event.creator, self.user)

    def test_create_invitation(self):
        invitee = User.objects.create_user(username='invitee', password='12345')
        invitation = Invitation.objects.create(event=self.event, invitee=invitee)
        self.assertEqual(invitation.event, self.event)
        self.assertEqual(invitation.invitee, invitee)


class SerializerTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.event_data = {
            'title': 'Sample Event',
            'description': 'Sample Description',
            'date': "2000-12-30T11:00:00Z",
            'creator': self.user
        }
        self.event = Event.objects.create(**self.event_data)
        self.invitation_data = {
            'event': self.event,
            'invitee': self.user
        }

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], self.user_data['username'])
        self.assertEqual(serializer.data['email'], self.user_data['email'])
        data = {'title': 'New Event', 'description': 'New Description', 'date': '2024-01-01T00:00', 'creator': self.user.id}
        serializer = EventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        new_event = serializer.save(creator=self.user)
        self.assertEqual(Event.objects.get(id=new_event.id).title, 'New Event')


    def test_event_serializer(self):
        serializer = EventSerializer(instance=self.event)
        self.assertEqual(serializer.data['title'], self.event_data['title'])
        data = {'title': 'New Event', 'description': 'New Description', 'date': '2023-12-31 00:00'}
        serializer = EventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        new_event = serializer.save(creator=self.user)
        self.assertEqual(Event.objects.get(id=new_event.id).title, 'New Event')
    def test_invitation_serializer(self):
        data = {'event': self.event.id, 'invitee': self.user.id}
        serializer = InvitationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'password': '12345', 'email': 'test@example.com'}

    def test_user_signup(self):
        response = self.client.post(reverse('user_signup'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.client.post(reverse('user_signup'), self.user_data, format='json')
        response = self.client.post(reverse('user_login'), {'username': 'testuser', 'password': '12345'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

class EventAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.event_data = {'title': 'New Event', 'description': 'Event Description', 'date': '2023-12-31 00:00'}

    def test_create_event(self):
        response = self.client.post(reverse('create_event'), self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_event(self):
        event = Event.objects.create(**self.event_data, creator=self.user)
        update_data = {'title': 'Updated Title', 'description': event.description, 'date': event.date}
        response = self.client.put(reverse('update_event', args=[event.id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        event = Event.objects.create(**self.event_data, creator=self.user)
        response = self.client.delete(reverse('delete_event', args=[event.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class InvitationAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.creator = User.objects.create_user(username='creator', password='pass123')
        self.invitee = User.objects.create_user(username='invitee', password='pass123')
        self.event = Event.objects.create(title='Sample Event', description='Event Description', date='2023-12-31 00:00', creator=self.creator)
        self.invite_url = reverse('invite_to_event')

    def test_create_invitation(self):
        self.client.force_authenticate(user=self.creator)
        invitation_data = {
            'event_id': self.event.id,
            'invitee': self.invitee.id
        }
        response = self.client.post(self.invite_url, invitation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_create_invitation_unauthorized(self):
        self.client.force_authenticate(user=self.invitee)
        invitation_data = {
            'event_id': self.event.id,
            'invitee': self.invitee.id
        }
        response = self.client.post(self.invite_url, invitation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invitation_for_nonexistent_event(self):
        self.client.force_authenticate(user=self.creator)
        invitation_data = {
            'event_id': 999, 
            'invitee_id': self.invitee.id
        }
        response = self.client.post(self.invite_url, invitation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)