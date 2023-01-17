from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from emenu.notifications.email import EmailSender
from emenu.notifications.notification_common import get_message
from emenu.notifications.sender_manager import SenderManager


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--email", help="Send a test email to indicated email address."
        )

    def handle(self, *args, **kwargs):
        email = kwargs.get("email")
        if not email:
            User = get_user_model()
            user = User.objects.all().first()
            if not user:
                self.stdout.write("Lack of users in database. Email has not been sent.")
                return
            email = user.email

        message = get_message()
        if not message:
            self.stdout.write("Lack of new or updated dishes. Email has not been sent.")
            return
        email_sender = EmailSender()
        notification_sender = SenderManager(
            notification_sender=email_sender, message=message
        )

        notification_sender.send(recipient_email=email)
