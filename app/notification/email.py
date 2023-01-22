import logging
from smtplib import SMTPAuthenticationError, SMTPSenderRefused, SMTPServerDisconnected

from django.conf import settings
from django.core.mail import send_mail

from emenu.utils import retry
from notification.notification_common import NotificationSender

logger = logging.getLogger(__name__)


class EmailSender(NotificationSender):
    @retry(retry_exceptions=(SMTPServerDisconnected,))
    def send(self, message: str, title: str, recipient_email: str) -> None:
        try:
            send_mail(
                subject=title,
                message=message,
                html_message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
            )
        except SMTPAuthenticationError as err:
            logger.exception("Authentication failed.")
            raise err
        except SMTPSenderRefused as err:
            logger.exception("Invalid MAIL FROM address.")
            raise err
