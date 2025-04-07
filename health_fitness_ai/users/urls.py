from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
     path('dashboard/', views.dashboard_view, name='dashboard'),
     path('', views.home_view, name='home'),
      path('notify/', views.notify_user_signup, name='notify_user_signup'),
      path('verify-email/', views.verify_email, name='verify_email'),
]

