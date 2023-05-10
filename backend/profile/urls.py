from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.UserProfile.as_view({'put': 'perform_update'})),
]

