# notifications/views.py
from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    # Mark all as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications/notifications.html', {
        'notifications': notifications
    })
