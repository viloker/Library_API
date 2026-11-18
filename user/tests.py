from django.test import TestCase

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from user.serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class UserManagerTests(TestCase):

    def test_create_user_success(self):
        user = User.objects.create_user(
            email="test@gmail.com",
            password="testpassword",
        )

        user_from_db = User.objects.get(email="test@gmail.com")

        self.assertEqual(user_from_db, user)
        self.assertEqual("test@gmail.com", user.email)
        self.assertTrue(user.check_password("testpassword"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_success(self):
        superuser = User.objects.create_superuser(
            email="superuser@gmail.com",
            password="superuserpassword",
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class UserAPITests(APITestCase):

    def setUp(self):
        self.register_url = "/users/"
        self.get_token_url = "/users/token/"
        self.refresh_token_url = "/users/token/refresh/"
        self.me_url = "/users/me/"

    def test_register_user_success(self):
        data = {"email": "test@gmail.com", "password": "testpassword"}

        response = self.client.post(self.register_url, data)

        user = User.objects.get(email="test@gmail.com")
        serializer = RegisterSerializer(user)

        self.assertEqual(201, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertTrue(user.check_password(data.get("password")))

    def test_get_user_token_success(self):
        data = {"email": "test@gmail.com", "password": "testpassword"}
        User.objects.create_user(**data)

        response = self.client.post(self.get_token_url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertIn("access", response.data.keys())
        self.assertIn("refresh", response.data.keys())

    def test_get_user_token_fail(self):
        data = {"email": "nonexistent@gmail.com", "password": "wrongpassword"}

        response = self.client.post(self.get_token_url, data)

        self.assertEqual(401, response.status_code)

    def test_refresh_user_token_success(self):
        data = {"email": "test@gmail.com", "password": "testpassword"}
        User.objects.create_user(**data)

        token_response = self.client.post(self.get_token_url, data)
        refresh_token = token_response.data.get("refresh")

        refresh_response = self.client.post(
            self.refresh_token_url, {"refresh": refresh_token}
        )

        self.assertEqual(200, refresh_response.status_code)
        self.assertIn("access", refresh_response.data.keys())

    def test_get_me_unauthenticated_401_error(self):
        response = self.client.get(self.me_url)

        self.assertEqual(401, response.status_code)

    def test_get_me_authenticated_success(self):
        data = {"email": "test@gmail.com", "password": "testpassword"}

        user = User.objects.create_user(**data)
        serializer = UserSerializer(user)

        token_response = self.client.post(self.get_token_url, data)
        token = token_response.data.get("access")

        me_response = self.client.get(self.me_url, HTTP_AUTHORIZE=f"Bearer {token}")

        self.assertEqual(200, me_response.status_code)
        self.assertEqual(serializer.data, me_response.data)
        self.assertNotIn("password", me_response.data.keys())
