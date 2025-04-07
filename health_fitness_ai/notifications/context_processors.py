# notifications/context_processors.py
from .models import Notification

def notification_status(request):
    if request.user.is_authenticated:
        has_new = Notification.objects.filter(user=request.user, is_read=False).exists()
        return {'has_new_notifications': has_new}
    return {}
