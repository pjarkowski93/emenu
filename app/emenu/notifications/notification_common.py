from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from django.db.models import Q

from emenu.models import Dish
from emenu.serializers import DishSerializer


class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str, recipient_email: str) -> None:
        raise NotImplementedError


def get_message() -> str:
    yesterday_datetime = datetime.today() - timedelta(days=1)
    year = yesterday_datetime.year
    month = yesterday_datetime.month
    day = yesterday_datetime.day
    dish_data = Dish.objects.filter(
        Q(created_at__year=year, created_at__month=month, created_at__day=day)
        | Q(updated_at__year=year, updated_at__month=month, updated_at__day=day)
    )
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

    return "".join(html_message)
