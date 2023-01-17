from smtplib import SMTPAuthenticationError, SMTPSenderRefused
from unittest.mock import call, patch

from django.test import override_settings, TestCase

from emenu.notifications.email import EmailSender

PATCHING_PATH = "emenu.notifications.email"


class EmailSenderTestCase(TestCase):
    @patch(f"{PATCHING_PATH}.send_mail")
    @patch(f"{PATCHING_PATH}.logger")
    @override_settings(EMAIL_HOST_USER="test@test_email.com")
    def test_send(self, mock_logger, mock_send_mail):
        message = "message"
        recipient_email = "test_email@test_email.com"
        message_to_send = f"""
        <html>
            <body>
            <p>Dish update</p>
                {message}
            </body>
        </html>
        """

        email_sender = EmailSender()
        email_sender.send(message=message, recipient_email=recipient_email)

        mock_logger.assert_not_called()
        mock_send_mail.assert_called_once_with(
            subject="Dish update",
            message="",
            html_message=message_to_send,
            from_email="test@test_email.com",
            recipient_list=[recipient_email],
        )

    @patch(f"{PATCHING_PATH}.send_mail")
    @patch(f"{PATCHING_PATH}.logger")
    @override_settings(EMAIL_HOST_USER="test@test_email.com")
    def test_send_with_empty_message(self, mock_logger, mock_send_mail):
        message = ""
        recipient_email = "test_email@test_email.com"

        email_sender = EmailSender()
        email_sender.send(message=message, recipient_email=recipient_email)

        self.assertEqual(
            mock_logger.mock_calls,
            [call.info("Lack of new or updated dishes. Email has not been sent.")],
        )
        mock_send_mail.assert_not_called()

    @patch(f"{PATCHING_PATH}.send_mail")
    @patch(f"{PATCHING_PATH}.logger")
    @override_settings(EMAIL_HOST_USER="test@test_email.com")
    def test_send_raise_auth_error(self, mock_logger, mock_send_mail):
        message = "message"
        recipient_email = "test_email@test_email.com"
        message_to_send = f"""
        <html>
            <body>
            <p>Dish update</p>
                {message}
            </body>
        </html>
        """
        mock_send_mail.side_effect = (
            SMTPAuthenticationError(code=401, msg="SMTP Authentication failed."),
        )

        email_sender = EmailSender()
        with self.assertRaises(
            SMTPAuthenticationError, msg="SMTP Authentication failed."
        ):
            email_sender.send(message=message, recipient_email=recipient_email)
        self.assertEqual(
            mock_logger.mock_calls, [call.exception("Authentication failed.")]
        )
        mock_send_mail.assert_called_once_with(
            subject="Dish update",
            message="",
            html_message=message_to_send,
            from_email="test@test_email.com",
            recipient_list=[recipient_email],
        )

    @patch(f"{PATCHING_PATH}.send_mail")
    @patch(f"{PATCHING_PATH}.logger")
    @override_settings(EMAIL_HOST_USER="test@test_email.com")
    def test_send_raise_sender_refused_error(self, mock_logger, mock_send_mail):
        message = "message"
        recipient_email = "test_email@test_email.com"
        message_to_send = f"""
        <html>
            <body>
            <p>Dish update</p>
                {message}
            </body>
        </html>
        """
        mock_send_mail.side_effect = (
            SMTPSenderRefused(
                code=400, msg=b"Invalid MAIL FROM address.", sender=recipient_email
            ),
        )

        email_sender = EmailSender()
        with self.assertRaises(SMTPSenderRefused, msg=b"Invalid MAIL FROM address."):
            email_sender.send(message=message, recipient_email=recipient_email)
        self.assertEqual(
            mock_logger.mock_calls, [call.exception("Invalid MAIL FROM address.")]
        )
        mock_send_mail.assert_called_once_with(
            subject="Dish update",
            message="",
            html_message=message_to_send,
            from_email="test@test_email.com",
            recipient_list=[recipient_email],
        )
