from django.urls import path
from . import views

urlpatterns = [
      path('meal-log/', views.meal_log_view, name='meal_log'),
      path('dashboard/', views.dashboard, name='dashboard'),
]
