# events/views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import User, Userlist, Event, Base
import binascii
import os

def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()

def get_session():
    engine = create_engine('postgresql+psycopg2://postgres:fgrr44xs00!M@localhost/eventsdb')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        data = {
            'username': request.query_params.get('username'),
            'name': request.query_params.get('name'),
            'surname': request.query_params.get('surname'),
            'password': request.query_params.get('password'),
        }
        session = get_session()
        token = generate_key()
        user = session.query(User).filter_by(token=token).first()
        if user:
            token = generate_key()
        new_user = User(username=data['username'], name=data['name'], surname=data['surname'], password=data['password'], token=token)
        try:
            session.add(new_user)
            session.commit()
            session.close()
            return Response({'message': 'User created successfully. Login to get the token.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error creating user: {e}")
            return Response({'message': 'Error creating user'}, status=status.HTTP_500_ITERNAL_SERVER_ERROR)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        session = get_session()
        data = {
            'username': request.query_params.get('username'),
            'password': request.query_params.get('password'),
        }
        user = session.query(User).filter_by(username=data['username'], password=data['password']).first()
        if user:
            return Response({'message': 'User logged in successfully', 'token': user.token}, status=status.HTTP_200_OK)
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_event(request, token):
    if request.method == 'POST':
        session = get_session()
        user = session.query(User).filter_by(token=token).first()
        if user:
            data = {
                'title': request.query_params.get('title'),
                'description': request.query_params.get('description'),
                'event_date': request.query_params.get('event_date'),
            }
            new_event = Event(title=data['title'], description=data['description'], created_by=user.username , event_date=data['event_date'])
            session.add(new_event)
            new_userlist = Userlist(title=data['title'], username=user.username)
            session.add(new_userlist)
            session.commit()
            session.close()
        return Response({'message': 'Event created successfully'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_events(request, token):
    if request.method == 'GET':
        session = get_session()
        user = session.query(User).filter_by(token=token).first()
        if user:
            events = session.query(Event).filter_by(created_by=user.username).all()
            if events:
                serialized_events = []
                for event in events:
                    serialized_event = {
                        'id': event.id,
                        'title': event.title,
                        'description': event.description,
                        'event_date': event.event_date
                    }
                    serialized_events.append(serialized_event)
                session.close()
                return Response(serialized_events, status=status.HTTP_200_OK)
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Access Denied'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_event(request, token, event_title):
    if request.method == 'PUT':
        session = get_session()
        user = session.query(User).filter_by(token=token).first()

        if not user:
            return Response({'message': 'Access Denied'}, status=status.HTTP_401_UNAUTHORIZED)

        event = session.query(Event).filter_by(title=event_title).first()

        if not event:
            return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'title': request.query_params.get('title'),
            'description': request.query_params.get('description'),
            'event_date': request.query_params.get('event_date'),
        }
        new_event = Event(title=data['title'], description=data['description'], created_by=event.created_by, event_date=data['event_date'])

        userlists = session.query(Userlist).filter_by(title=event_title).all()
        for userlist in userlists:
            session.delete(userlist)
        session.commit()
        session.delete(event)
        session.commit()
        session.add(new_event)
        session.commit()
        for userlist in userlists:
            new_userlist = Userlist(title=data['title'], username=userlist.username)
            session.add(new_userlist)
        session.commit()
        session.close()
        return Response({'message': 'Event updated successfully'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_event(request, token, event_title):
    if request.method == 'DELETE':
        session = get_session()
        user = session.query(User).filter_by(token=token).first()
        if user:
            userlists = session.query(Userlist).filter_by(title=event_title).all()
            if not userlists:
                return Response({'message': 'Userlist not found'}, status=status.HTTP_404_NOT_FOUND)

            event = session.query(Event).filter_by(title=event_title).first()
            if not event:
                return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
            session.delete(event)
            session.commit()

            for userlist in userlists:
                session.delete(userlist)
                session.commit()
            session.close()
            return Response({'message': 'Event deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Access Denied'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_invitations(request, token):
    if request.method == 'GET':
        session = get_session()
        user = session.query(User).filter_by(token=token).first()
        if user:
            userlists = session.query(Userlist).filter_by(username=user.username).all()
            if userlists:
                serialized_events = []
                for userlist in userlists:
                    event = userlist.events
                    serialized_event = {
                        'id': event.id,
                        'title': event.title,
                        'description': event.description,
                        'created_by': event.created_by,
                        'event_date': event.event_date
                    }
                    serialized_events.append(serialized_event)
                session.close()
                return Response(serialized_events, status=status.HTTP_200_OK)
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Access Denied'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def event_invited_users(request, event_title):
    if request.method == 'GET':
        session = get_session()
        userlists = session.query(Userlist).filter_by(title=event_title).all()
        if not userlists:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serialized_invited_users = []
        for userlist in userlists: 
            user = userlist.user
            serialized_invited_users.append({'username': user.username, 'name': user.name, 'surname': user.surname})
        session.close()
        return Response(serialized_invited_users, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def invite_user(request, token, event_title):
    if request.method == 'POST':
        session = get_session()
        user = session.query(User).filter_by(token=token).first()
        if user:
            event = session.query(Event).filter_by(title=event_title, created_by=user.username).first()
            if not event:
                return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
            data = {
                'username': request.query_params.get('username')
            }
            invited_user = session.query(User).filter_by(username=data['username']).first()
            if invited_user:
                new_userlist = Userlist(title=event_title, username=data['username'])
                session.add(new_userlist)
                session.commit()
                session.close()
                return Response({'message': 'User added to event successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invited user not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Access Denied'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

