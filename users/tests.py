# users/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITests(APITestCase):

    def setUp(self):
        """
        Create test users
        """
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="AdminPass123"
        )

        self.user = User.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="UserPass123"
        )

        self.register_url = "/api/users/"
        self.token_url = "/api/auth/token/"
        self.me_url = "/api/users/me/"

    # -------------------------
    # AUTHENTICATION TESTS
    # -------------------------

    def test_user_login_jwt(self):
        """
        User can obtain JWT token
        """
        response = self.client.post(self.token_url, {
            "username": "user1",
            "password": "UserPass123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_credentials(self):
        response = self.client.post(self.token_url, {
            "username": "user1",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------------------------
    # USER REGISTRATION
    # -------------------------

    def test_user_registration(self):
        """
        New user can register
        """
        data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!"
        }

        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_registration_password_mismatch(self):
        data = {
            "username": "baduser",
            "email": "bad@test.com",
            "password": "Pass12345",
            "password2": "DifferentPass"
        }

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------
    # PROFILE & ME ENDPOINT
    # -------------------------

    def test_authenticated_user_can_access_me(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_unauthenticated_user_cannot_access_me(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------------------------
    # ADMIN PERMISSIONS
    # -------------------------

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_non_admin_cannot_list_users(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_user(self):
        self.client.force_authenticate(user=self.admin)

        url = f"{self.register_url}{self.user.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_admin_cannot_delete_user(self):
        self.client.force_authenticate(user=self.user)

        url = f"{self.register_url}{self.admin.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
