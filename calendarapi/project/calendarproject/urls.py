#urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', views.UserSignUp.as_view(), name='user_signup'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('event/create/', views.CreateEvent.as_view(), name='create_event'),
    path('event/update/<int:pk>/', views.UpdateEvent.as_view(), name='update_event'),
    path('event/delete/<int:pk>/', views.DeleteEvent.as_view(), name='delete_event'),
    path('event/invite/', views.InviteToEvent.as_view(), name='invite_to_event'),
    path('events/created/', views.ViewCreatedEvents.as_view(), name='view_created_events'),
    path('events/invited/', views.ViewEventUserInvitedTo.as_view(), name='view_event_user_invited_to'),
    path('event/invited-users/<int:event_id>/', views.ViewUsersInvitedToEvent.as_view(), name='view_users_invited_to_event'),
]
