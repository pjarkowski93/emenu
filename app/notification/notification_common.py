from abc import ABC, abstractmethod

from emenu.models import Dish
from emenu.serializers import DishSerializer
from notification.exceptions import LackOfMessageDataException


class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str, title: str, recipient_email: str) -> None:
        raise NotImplementedError


def get_email_data() -> dict:
    dish_data = Dish.get_notification_dishes()
    if not dish_data:
        raise LackOfMessageDataException("Nothing to send.")
    message_data = DishSerializer(dish_data, many=True).data

    html_message = (
        f"""
            <li>Name: {data['name']}</li>
            <li>Price: {data['price']}</li>
            <li>Description: {data['description']}</li>
            <li>{'Is vegetarian' if data['is_vegetarian'] else 'Is not vegetarian'}</li>
            <li>Preparing time: {data['preparing_time']}</li>
            <br></br>
        """
        for data in message_data
    )

    return {"message": "".join(html_message)}
