from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.FriendChannels.as_view()),
    path('group/', views.GroupChannels.as_view()),
    path('messages/<channel_id>', views.Messages.as_view())
]




