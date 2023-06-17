from django.urls import path, include
from . import views

urlpatterns = [
    path('latest/', views.FriendRequests.as_view()),
    path('<username>', views.FriendRequests.as_view()),
    path('create/', views.FriendRequests.as_view()),
    path('set/', views.FriendApprover.as_view()),
]

