from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, UserProfileForm
from django.core.signing import Signer, BadSignature
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.signing import Signer
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

# Register view with email verification
def register_view(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data['email']
            
            # Check if email already exists
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "This email is already registered.")
                return redirect('register')  # Redirect back to the registration page
            
            # Proceed with user registration
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = False  # User is not active until email is verified
            user.save()

            # Create user profile and link to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Email verification
            signer = Signer()
            token = signer.sign(user.email)

            verification_url = request.build_absolute_uri(
                reverse('verify_email') + f'?token={token}'
            )

            send_mail(
                subject='Confirm Your Email – Health & Fitness App',
                message=f'Hi {user.username},\n\nPlease verify your email by clicking the link below:\n\n{verification_url}\n\nThanks!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return render(request, "users/verify_notice.html", {"email": user.email})
    else:
        user_form = RegisterForm()
        profile_form = UserProfileForm()

    return render(request, "users/register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

# Email confirmation view
def verify_email(request):
    # Retrieve the token from the query parameter
    token = request.GET.get('token')

    if not token:
        return render(request, 'users/invalid_token.html')

    signer = Signer()

    try:
        email = signer.unsign(token)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        login(request, user)

        # Send final welcome mail after confirmation
        send_mail(
            subject='🎉 Welcome to Health & Fitness App!',
            message='Your email has been verified. You can now start using all features!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return render(request, 'users/email_verified.html')

    except (BadSignature, User.DoesNotExist):
        return render(request, 'users/invalid_token.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  # If user is valid
            login(request, user)  # Log the user in
            messages.success(request, "Successfully logged in!")
            return redirect('dashboard')  # Redirect to the main dashboard
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to login page

    return render(request, 'users/login.html')

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile view
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})

# Dashboard view
@login_required
def dashboard_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {'profile': profile})  # or any relevant template

# Home view
def home_view(request):
    return render(request, 'users/home.html')

# Notify user signup using Supabase (example feature)
from .supabase_client import supabase

@login_required
def notify_user_signup(request):
    email = request.user.email  # Get email from logged-in user

    data = {
        "email": email,
        "message": "Welcome to your fitness coach platform!"
    }

    # Insert notification data into Supabase
    supabase.table("notifications").insert(data).execute()

    return render(request, 'users/email_sent.html')
def loader_view(request):
    return render(request, 'users/loader.html')