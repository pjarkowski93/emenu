from datetime import datetime, timedelta
from urllib.parse import urlencode

from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from parameterized import param, parameterized
from rest_framework.test import APIClient

from emenu.models import Dish


def _params_for_filter():
    yesterday_datetime = datetime.today() - timedelta(days=1)
    tomorrow_datetime = datetime.today() + timedelta(days=1)
    yesterday = yesterday_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    tomorrow = tomorrow_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return [
        param(
            "name",
            filter_params={"name": "dish_name"},
            expected_count=1,
            expected_result={
                "field_name": "name",
                "field_value": "dish_name",
                "method": "assertEqual",
            },
        ),
        param(
            "price_lte",
            filter_params={"price_lte": 15.00},
            expected_count=2,
            expected_result={
                "field_name": "price",
                "field_value": 15,
                "method": "assertLessEqual",
            },
        ),
        param(
            "price_gt",
            filter_params={"price_gt": 20.00},
            expected_count=2,
            expected_result={
                "field_name": "price",
                "field_value": 20,
                "method": "assertGreater",
            },
        ),
        param(
            "preparing_time_lte",
            filter_params={"preparing_time_lte": 35},
            expected_count=3,
            expected_result={
                "field_name": "preparing_time",
                "field_value": 35,
                "method": "assertLessEqual",
            },
        ),
        param(
            "preparing_time_gt",
            filter_params={"preparing_time_gt": 35},
            expected_count=3,
            expected_result={
                "field_name": "preparing_time",
                "field_value": 35,
                "method": "assertGreater",
            },
        ),
        param(
            "is_vegetarian_true",
            filter_params={"is_vegetarian": True},
            expected_count=3,
            expected_result={
                "field_name": "is_vegetarian",
                "field_value": True,
                "method": "assertTrue",
            },
        ),
        param(
            "is_vegetarian_false",
            filter_params={"is_vegetarian": False},
            expected_count=3,
            expected_result={
                "field_name": "is_vegetarian",
                "field_value": False,
                "method": "assertFalse",
            },
        ),
        param(
            "created_at_lte",
            filter_params={"created_at_lte": yesterday},
            expected_count=0,
            expected_result={
                "field_name": "created_at",
                "field_value": [],
                "method": "assertEqual",
            },
        ),
        param(
            "created_at_gt",
            filter_params={"created_at_gt": yesterday},
            expected_count=6,
            expected_result={
                "field_name": "created_at",
                "field_value": yesterday,
                "method": "assertGreater",
            },
        ),
        param(
            "updated_at_lte",
            filter_params={"updated_at_lte": tomorrow},
            expected_count=6,
            expected_result={
                "field_name": "updated_at",
                "field_value": tomorrow,
                "method": "assertLessEqual",
            },
        ),
        param(
            "updated_at_gt",
            filter_params={"updated_at_gt": tomorrow},
            expected_count=0,
            expected_result={
                "field_name": "updated_at",
                "field_value": [],
                "method": "assertEqual",
            },
        ),
    ]


class DishFiltersTestCase(TestCase):
    def setUp(self) -> None:
        baker.generators.add("djmoney.models.fields.MoneyField", lambda: "100.00")
        self.api_client = APIClient()
        baker.make(
            Dish, name="dish_name", price=10.00, preparing_time=40, is_vegetarian=True
        )
        baker.make(Dish, price=20.00, preparing_time=45, is_vegetarian=False)
        baker.make(Dish, price=10.00, preparing_time=30, is_vegetarian=True)
        baker.make(Dish, price=15.50, preparing_time=30, is_vegetarian=True)
        baker.make(Dish, price=20.20, preparing_time=45, is_vegetarian=False)
        baker.make(Dish, price=25.00, preparing_time=35, is_vegetarian=False)

    @parameterized.expand(_params_for_filter)
    def test_filter_dish(
        self, _, filter_params: dict, expected_count: int, expected_result: dict
    ):
        _url = reverse("dish-list")
        url = f"{_url}?{urlencode(filter_params)}"
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), expected_count)
        method_to_compare = getattr(self, expected_result["method"])
        for data in response.data:
            if expected_result["field_name"] == "price":
                method_to_compare(
                    float(data[expected_result["field_name"]]),
                    expected_result["field_value"],
                )
            else:
                method_to_compare(
                    data[expected_result["field_name"]], expected_result["field_value"]
                )
