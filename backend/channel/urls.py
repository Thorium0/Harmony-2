from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.FriendChannels.as_view()),
    path('messages/<channel_name>', views.Messages.as_view())
]




