from unittest.mock import Mock, patch

from django.test import TestCase

from notification.notification_common import get_email_data

PATCHING_PATH = "notification.notification_common"


class GetMessageTestCase(TestCase):
    @patch(f"{PATCHING_PATH}.Dish")
    @patch(f"{PATCHING_PATH}.DishSerializer")
    def test_get_email_message(self, mock_DishSerializer, mock_Dish):
        mock_Dish.get_notification_dishes.return_value = ["data"]
        serializer_data = [
            {
                "name": "test_name1",
                "price": 100.00,
                "description": "test_description1",
                "is_vegetarian": True,
                "preparing_time": 30,
            },
            {
                "name": "test_name2",
                "price": 100.00,
                "description": "test_description2",
                "is_vegetarian": True,
                "preparing_time": 30,
            },
            {
                "name": "test_name3",
                "price": 100.00,
                "description": "test_description3",
                "is_vegetarian": False,
                "preparing_time": 30,
            },
        ]
        mock_serializer_data = Mock()
        mock_serializer_data.data = serializer_data
        mock_DishSerializer.return_value = mock_serializer_data

        message = get_email_data()
        mock_Dish.get_notification_dishes.assert_called_once_with()
        mock_DishSerializer.assert_called_once_with(["data"], many=True)
        for data in serializer_data:
            assert data["name"] in message["message"]
            assert data["name"] in message["message"]
            assert str(data["price"]) in message["message"]
            assert data["description"] in message["message"]
            assert str(data["preparing_time"]) in message["message"]
            if data["is_vegetarian"]:
                assert "Is vegetarian" in message["message"]
            else:
                assert "Is not vegetarian" in message["message"]
