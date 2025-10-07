from .models import Notification

def notify(recipient, message, url="", type="INFO"):
    if recipient is None:
        return None
    return Notification.objects.create(recipient=recipient, message=message, url=url, type=type)
