from django.contrib.auth import get_user_model

from emenu.notifications.email import EmailSender
from emenu.notifications.notification_common import get_message
from emenu.notifications.sender_manager import SenderManager


def send_dish_updates():
    User = get_user_model()
    user_emails = User.objects.all().values_list("email", flat=True)
    message = get_message()
    email_sender = EmailSender()
    notification_sender = SenderManager(
        notification_sender=email_sender, message=message
    )
    for email in user_emails:
        notification_sender.send(recipient_email=email)
