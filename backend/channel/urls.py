from django.urls import path, include
from . import views

urlpatterns = [
    #path('latest/', views.LatestChannelsList.as_view()),
    path('', views.FriendChannels.as_view()),
    #path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
]




