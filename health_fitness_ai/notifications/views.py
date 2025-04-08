from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Mark all as read
    notifications.update(is_read=True)

    return render(request, 'notifications/notifications.html', {
        'notifications': notifications
    })

@login_required
def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return redirect('notification_list')
