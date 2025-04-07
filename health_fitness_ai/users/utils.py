# users/utils.py

from .supabase_client import supabase

def send_signup_notification(email):
    supabase.table("notifications").insert({
        "email": email,
        "message": "🎉 Welcome to your fitness platform!"
    }).execute()
