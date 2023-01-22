# from unittest.mock import call, Mock, patch

# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from model_bakery import baker

# from notification.tasks.notifications import send_email

# PATCHING_PATH = "notification.tasks.notifications"


# class SendDishUpdatesTestCase(TestCase):
#     @patch(f"{PATCHING_PATH}.get_email_message")
#     @patch(f"{PATCHING_PATH}.EmailSender")
#     @patch(f"{PATCHING_PATH}.SenderManager")
#     def test_send_dish_updates(
#         self,
#         mock_SenderManager,
#         mock_EmailSender,
#         mock_get_email_message,
#     ):
#         User = get_user_model()
#         baker.make(User, email="test_email1@test_email.com")
#         baker.make(User, email="test_email2@test_email.com")

#         mock_EmailSender.return_value = None
#         mock_send = Mock()
#         mock_send.send.return_value = None
#         mock_SenderManager.return_value = mock_send
#         mock_get_email_message.return_value = "test_message"

#         send_email()

#         mock_EmailSender.assert_called_once_with()
#         mock_SenderManager.assert_called_once_with(
#             notification_sender=None, message="test_message"
#         )
#         self.assertEqual(
#             mock_send.mock_calls,
#             [
#                 call.send(recipient_email="test_email1@test_email.com"),
#                 call.send(recipient_email="test_email2@test_email.com"),
#             ],
#         )
