from unittest.mock import Mock, patch

from django.test import TestCase

from emenu.notifications.notification_common import get_message

PATCHING_PATH = "emenu.notifications.notification_common"


class GetMessageTestCase(TestCase):
    @patch(f"{PATCHING_PATH}.Dish")
    @patch(f"{PATCHING_PATH}.DishSerializer")
    def test_get_message(self, mock_DishSerializer, mock_Dish):
        mock_Dish.objects.filter.return_value = []
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

        message = get_message()
        self.assertEqual(mock_Dish.objects.filter.call_count, 1)
        mock_DishSerializer.assert_called_once_with([], many=True)
        for data in serializer_data:
            assert data["name"] in message
            assert data["name"] in message
            assert str(data["price"]) in message
            assert data["description"] in message
            assert str(data["preparing_time"]) in message
            if data["is_vegetarian"]:
                assert "Is vegetarian" in message
            else:
                assert "Is not vegetarian" in message
