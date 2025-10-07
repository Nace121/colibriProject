from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Notification

@login_required
def notification_list(request):
    qs_unread = Notification.objects.filter(recipient=request.user, is_read=False)
    qs_read = Notification.objects.filter(recipient=request.user, is_read=True)[:50]
    return render(request, "notifications/list.html", {"unread": qs_unread, "read": qs_read})

@login_required
def notification_read(request, notification_id):
    n = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    n.mark_read()
    if n.url:
        return redirect(n.url)
    return redirect("notifications:list")

@login_required
def notification_read_all(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect("notifications:list")
