from model_bakery import baker
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from emenu.models import Dish, Menu, MenuDishMap


class MenuViewSetTestCase(TestCase):
    def setUp(self) -> None:
        baker.generators.add("djmoney.models.fields.MoneyField", lambda: "100.00")
        self.api_client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(
            "test_user", "test_user@email.com", "testuser123"
        )
        self.menu_list_url = reverse("menu-list")

    def test_create_menu(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(
            self.menu_list_url, data={"name": "test name menu"}, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "test name menu")

    def test_create_menu_without_name(self):
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.menu_list_url, data={}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["name"][0].code, "required")
        self.assertEqual(response.data["name"][0].title(), "This Field Is Required.")

    def test_create_menu_without_authentication(self):
        response = self.api_client.post(self.menu_list_url, data={}, format="json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"].code, "not_authenticated")
        self.assertEqual(
            response.data["detail"].title(),
            "Authentication Credentials Were Not Provided.",
        )

    def test_get_menu_without_dishes(self):
        baker.make(Menu)
        response = self.api_client.get(self.menu_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_menu_with_dishes(self):
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        baker.make(MenuDishMap, menu=menu, dish=dish)
        response = self.api_client.get(self.menu_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["uuid"], str(menu.uuid))
        self.assertEqual(response.data[0]["name"], menu.name)
        self.assertEqual(len(response.data[0]["dishes"]), 1)
        self.assertEqual(response.data[0]["dishes"][0]["name"], dish.name)
        self.assertEqual(response.data[0]["dishes"][0]["price"], str(dish.price.amount))
        self.assertEqual(response.data[0]["dishes"][0]["description"], dish.description)
        self.assertEqual(
            response.data[0]["dishes"][0]["preparing_time"], dish.preparing_time
        )
        self.assertEqual(
            response.data[0]["dishes"][0]["is_vegetarian"], dish.is_vegetarian
        )
        self.assertEqual(
            response.data[0]["dishes"][0]["created_at"],
            dish.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(
            response.data[0]["dishes"][0]["updated_at"],
            dish.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
