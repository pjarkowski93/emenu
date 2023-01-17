from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from parameterized import parameterized
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

    @parameterized.expand(("post", "patch", "put", "delete"))
    def test_unauthorized_requests(self, method):
        url = reverse("dish-detail", kwargs={"uuid": str(uuid4())})
        if method == "post":
            url = self.menu_list_url

        request_method = getattr(self.api_client, method)
        response = request_method(url)

        self.assertEqual(response.status_code, 401)

    def test_get_menu_without_dishes(self):
        baker.make(Menu)
        response = self.api_client.get(self.menu_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_menu_with_dishes(self):
        menu = baker.make(Menu)
        baker.make(Menu)
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

    def test_get_single_menu_with_dishes(self):
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        baker.make(MenuDishMap, menu=menu, dish=dish)
        menu2 = baker.make(Menu)
        dish2 = baker.make(Dish)
        baker.make(MenuDishMap, menu=menu2, dish=dish2)
        detail_url = reverse("menu-detail", kwargs={"uuid": str(menu.uuid)})

        response = self.api_client.get(detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(menu.uuid))
        self.assertEqual(response.data["name"], menu.name)
        self.assertEqual(len(response.data["dishes"]), 1)
        self.assertEqual(response.data["dishes"][0]["name"], dish.name)
        self.assertEqual(response.data["dishes"][0]["price"], str(dish.price.amount))
        self.assertEqual(response.data["dishes"][0]["description"], dish.description)
        self.assertEqual(
            response.data["dishes"][0]["preparing_time"], dish.preparing_time
        )
        self.assertEqual(
            response.data["dishes"][0]["is_vegetarian"], dish.is_vegetarian
        )
        self.assertEqual(
            response.data["dishes"][0]["created_at"],
            dish.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(
            response.data["dishes"][0]["updated_at"],
            dish.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )

    def test_get_single_not_existing_menu_with_dishes(self):
        detail_url = reverse("menu-detail", kwargs={"uuid": str(uuid4())})

        response = self.api_client.get(detail_url)

        self.assertEqual(response.status_code, 404)

    def test_get_menu_details(self):
        menu = baker.make(Menu)
        dish = baker.make(Dish)
        baker.make(MenuDishMap, menu=menu, dish=dish)

        response = self.api_client.get(f"/menu/{menu.uuid}/menu_details/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(menu.uuid))
        self.assertEqual(response.data["name"], menu.name)
        self.assertEqual(
            response.data["created_at"],
            menu.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(
            response.data["updated_at"],
            menu.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(len(response.data["dishes"]), 1)
        self.assertEqual(response.data["dishes"][0]["name"], dish.name)
        self.assertEqual(response.data["dishes"][0]["price"], str(dish.price.amount))
        self.assertEqual(response.data["dishes"][0]["description"], dish.description)
        self.assertEqual(
            response.data["dishes"][0]["preparing_time"], dish.preparing_time
        )
        self.assertEqual(
            response.data["dishes"][0]["is_vegetarian"], dish.is_vegetarian
        )
        self.assertEqual(
            response.data["dishes"][0]["created_at"],
            dish.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(
            response.data["dishes"][0]["updated_at"],
            dish.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )

    def test_put_menu(self):
        menu = baker.make(Menu)
        self.api_client.force_authenticate(user=self.user)
        data_to_update = {
            "uuid": str(menu.uuid),
            "name": "new name",
            "created_at": menu.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": menu.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        detail_url = reverse("menu-detail", kwargs={"uuid": str(menu.uuid)})
        response = self.api_client.put(detail_url, data=data_to_update, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["name"], menu.name)
        self.assertEqual(response.data["name"], data_to_update["name"])
        self.assertEqual(response.data["created_at"], data_to_update["created_at"])
        self.assertNotEqual(response.data["updated_at"], data_to_update["updated_at"])

    def test_patch_menu(self):
        menu = baker.make(Menu)
        self.api_client.force_authenticate(user=self.user)
        data_to_update = {
            "name": "super new name",
        }
        detail_url = reverse("menu-detail", kwargs={"uuid": str(menu.uuid)})
        response = self.api_client.patch(detail_url, data=data_to_update, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["name"], menu.name)
        self.assertEqual(response.data["name"], data_to_update["name"])

    def test_delete_menu(self):
        menu = baker.make(Menu)
        self.api_client.force_authenticate(user=self.user)
        detail_url = reverse("menu-detail", kwargs={"uuid": str(menu.uuid)})
        response = self.api_client.delete(detail_url)

        self.assertEqual(response.status_code, 204)

        response_after_delete = self.api_client.delete(detail_url)

        self.assertEqual(response_after_delete.status_code, 404)
