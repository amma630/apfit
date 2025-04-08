# notifications/views.py
from django.shortcuts import render,redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    # Mark all as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications/notifications.html', {
        'notifications': notifications
    })
def dashboard(request):
    has_new_notifications = False
    if request.user.is_authenticated:
        has_new_notifications = Notification.objects.filter(user=request.user, is_read=False).exists()
    return render(request, 'users/base.html', {'has_new_notifications': has_new_notifications})


def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notification_list')