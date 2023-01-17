from datetime import datetime, timedelta
from urllib.parse import urlencode

from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from parameterized import param, parameterized
from rest_framework.test import APIClient

from emenu.models import Dish, Menu, MenuDishMap


def _params_for_filter():
    yesterday_datetime = datetime.today() - timedelta(days=1)
    tomorrow_datetime = datetime.today() + timedelta(days=1)
    yesterday = yesterday_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    tomorrow = tomorrow_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return [
        param(
            "created_at_lte",
            filter_params={"created_at_lte": yesterday},
            expected_count=0,
        ),
        param(
            "created_at_gt",
            filter_params={"created_at_gt": yesterday},
            expected_count=2,
        ),
        param(
            "updated_at_lte",
            filter_params={"updated_at_lte": tomorrow},
            expected_count=2,
        ),
        param(
            "updated_at_gt",
            filter_params={"updated_at_gt": tomorrow},
            expected_count=0,
        ),
    ]


class MenuFiltersTestCase(TestCase):
    def setUp(self) -> None:
        baker.generators.add("djmoney.models.fields.MoneyField", lambda: "100.00")
        self.api_client = APIClient()

        menu1 = baker.make(Menu, name="menu_name")
        menu2 = baker.make(Menu)
        baker.make(Menu)

        dish1 = baker.make(Dish)
        dish2 = baker.make(Dish)
        dish3 = baker.make(Dish)
        dish4 = baker.make(Dish)

        baker.make(MenuDishMap, menu=menu1, dish=dish1)
        baker.make(MenuDishMap, menu=menu1, dish=dish2)
        baker.make(MenuDishMap, menu=menu1, dish=dish3)
        baker.make(MenuDishMap, menu=menu2, dish=dish4)

    @parameterized.expand(_params_for_filter)
    def test_filter_by_dates(self, _, filter_params: dict, expected_count: int):
        _url = reverse("menu-list")
        url = f"{_url}?{urlencode(filter_params)}"
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), expected_count)

    @parameterized.expand(
        [
            param(
                "name",
                filter_params={"name": "menu_name"},
                expected_count=1,
                expected_result={
                    "field_name": "name",
                    "field_value": "menu_name",
                    "method": "assertEqual",
                },
            ),
            param(
                "dish_count",
                filter_params={"dish_count": 2},
                expected_count=1,
                expected_result={
                    "field_name": "dishes",
                    "field_value": 3,
                    "method": "assertEqual",
                },
            ),
        ]
    )
    def test_filter_menu(
        self, _, filter_params: dict, expected_count: int, expected_result: dict
    ):
        _url = reverse("menu-list")
        url = f"{_url}?{urlencode(filter_params)}"
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), expected_count)
        method_to_compare = getattr(self, expected_result["method"])
        for data in response.data:
            if expected_result["field_name"] == "dishes":
                self.assertEqual(len(data["dishes"]), expected_result["field_value"])
            else:
                method_to_compare(
                    data[expected_result["field_name"]], expected_result["field_value"]
                )
