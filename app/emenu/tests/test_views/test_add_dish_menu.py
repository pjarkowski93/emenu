from uuid import uuid4
from parameterized import parameterized
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from emenu.models import Dish, Menu, MenuDishMap


class AddDishToMenuViewSetTestCase(TestCase):
    def setUp(self) -> None:
        baker.generators.add("djmoney.models.fields.MoneyField", lambda: "100.00")
        self.api_client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(
            "test_user", "test_user@email.com", "testuser123"
        )

    def test_add_dish_to_menu(self):
        self.api_client.force_authenticate(user=self.user)
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        data = {"menu": str(menu.uuid), "dish": str(dish.uuid)}
        add_menu_dish_url = reverse("add_dish_to_menu")

        response = self.api_client.post(add_menu_dish_url, data=data, format="json")

        self.assertEqual(response.status_code, 201)

    def test_put_dish_to_menu(self):
        self.api_client.force_authenticate(user=self.user)
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        new_dish = baker.make(Dish)
        menu_dish_map = baker.make(MenuDishMap, menu=menu, dish=dish)
        data = {
            "uuid": str(menu_dish_map.uuid),
            "menu": str(menu.uuid),
            "dish": str(new_dish.uuid),
        }
        add_menu_dish_detail_url = reverse(
            "update_destroy_dish_menu", kwargs={"uuid": str(menu_dish_map.uuid)}
        )

        response = self.api_client.put(
            add_menu_dish_detail_url, data=data, format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_patch_dish_to_menu(self):
        self.api_client.force_authenticate(user=self.user)
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        new_dish = baker.make(Dish)
        menu_dish_map = baker.make(MenuDishMap, menu=menu, dish=dish)
        data = {
            "dish": str(new_dish.uuid),
        }
        add_menu_dish_detail_url = reverse(
            "update_destroy_dish_menu", kwargs={"uuid": str(menu_dish_map.uuid)}
        )

        response = self.api_client.patch(
            add_menu_dish_detail_url, data=data, format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_dish_to_menu(self):
        self.api_client.force_authenticate(user=self.user)
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        menu_dish_map = baker.make(MenuDishMap, menu=menu, dish=dish)
        add_menu_dish_detail_url = reverse(
            "update_destroy_dish_menu", kwargs={"uuid": str(menu_dish_map.uuid)}
        )

        response = self.api_client.delete(add_menu_dish_detail_url)

        self.assertEqual(response.status_code, 204)

        response = self.api_client.delete(add_menu_dish_detail_url)

        self.assertEqual(response.status_code, 404)

    def test_get_not_allowed(self):
        self.api_client.force_authenticate(user=self.user)
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        menu_dish_map = baker.make(MenuDishMap, menu=menu, dish=dish)
        add_menu_dish_detail_url = reverse(
            "update_destroy_dish_menu", kwargs={"uuid": str(menu_dish_map.uuid)}
        )

        response = self.api_client.get(add_menu_dish_detail_url)

        self.assertEqual(response.status_code, 405)

        add_menu_dish_url = reverse("add_dish_to_menu")

        response = self.api_client.delete(add_menu_dish_url)

        self.assertEqual(response.status_code, 405)

    @parameterized.expand(("post", "patch", "put", "delete"))
    def test_unauthorized_requests(self, method):
        url = reverse("update_destroy_dish_menu", kwargs={"uuid": str(uuid4())})
        if method == "post":
            url = reverse("add_dish_to_menu")

        request_method = getattr(self.api_client, method)
        response = request_method(url)

        self.assertEqual(response.status_code, 401)
