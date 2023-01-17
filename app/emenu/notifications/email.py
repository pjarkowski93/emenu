import logging
from smtplib import SMTPAuthenticationError, SMTPSenderRefused, SMTPServerDisconnected

from django.conf import settings
from django.core.mail import send_mail

from emenu.notifications.notification_common import NotificationSender
from emenu.utils import retry

logger = logging.getLogger(__name__)


class EmailSender(NotificationSender):
    @retry(retry_exceptions=(SMTPServerDisconnected,))
    def send(self, message: str, recipient_email: str) -> None:
        if not message:
            logger.info("Lack of new or updated dishes. Email has not been sent.")
            return
        message_to_send = f"""
        <html>
            <body>
            <p>Dish update</p>
                {message}
            </body>
        </html>
        """
        try:
            send_mail(
                subject="Dish update",
                message="",
                html_message=message_to_send,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
            )
        except SMTPAuthenticationError as err:
            logger.exception("Authentication failed.")
            raise err
        except SMTPSenderRefused as err:
            logger.exception("Invalid MAIL FROM address.")
            raise err
