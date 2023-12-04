from django.urls import path
from . import views

urlpatterns = [
    
    path('api/user/signup/', views.user_signup, name='user_signup'),
    path('api/user/login/', views.user_login, name='user_login'),
    path('api/user/<str:token>/invitations/', views.user_invitations, name='user_invitations'),
    path('api/events/<str:token>/create/', views.create_event, name='create_event'),
    path('api/events/<str:token>/list', views.user_events, name='user_events'),
    path('api/events/<str:token>/<str:event_title>/update/', views.update_event, name='update_event'),
    path('api/events/<str:token>/<str:event_title>/delete/', views.delete_event, name='delete_event'),
    path('api/events/<str:token>/<str:event_title>/invite/', views.invite_user, name='invite_user'),
    path('api/events/<str:event_title>/users/', views.event_invited_users, name='event_invited_users'),
]
