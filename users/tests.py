from rest_framework.test import APITestCase

from cart.models import Cart


class AuthenticationAPITests(APITestCase):
    def test_registration_creates_customer_and_cart(self):
        response = self.client.post(
            "/api/v1/users/register/",
            {
                "username": "new-shopper",
                "email": "new-shopper@example.com",
                "password": "safe-password-123",
                "phone_number": "123456789",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Cart.objects.filter(user__username="new-shopper").exists())

    def test_login_returns_access_token(self):
        self.client.post(
            "/api/v1/users/register/",
            {"username": "shopper", "email": "shopper@example.com", "password": "safe-password-123"},
            format="json",
        )

        response = self.client.post(
            "/api/v1/users/token/",
            {"username": "shopper", "password": "safe-password-123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_customer_can_read_and_update_only_own_profile(self):
        self.client.post(
            "/api/v1/users/register/",
            {"username": "profile-user", "email": "profile@example.com", "password": "safe-password-123"},
            format="json",
        )
        login = self.client.post(
            "/api/v1/users/token/",
            {"username": "profile-user", "password": "safe-password-123"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

        response = self.client.patch("/api/v1/users/me/", {"phone_number": "123456789"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["phone_number"], "123456789")
