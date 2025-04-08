# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('clear/', views.clear_notifications, name='clear_notifications'),
]
