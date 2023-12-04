#models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    creator = models.ForeignKey(User, related_name='created_events', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='events_participated')

    def __str__(self):
        return self.title

class Invitation(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, related_name='invitations', on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, related_name='invitations', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.title} - {self.invitee.username}"
