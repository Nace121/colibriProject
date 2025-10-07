from .models import Notification

def notifications_badge(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    else:
        count = 0
    return {"notifications_unread_count": count}
