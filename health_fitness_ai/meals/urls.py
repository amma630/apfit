from django.urls import path
from . import views

urlpatterns = [
    path('', views.meal_log_view, name='meal_log'),
]
