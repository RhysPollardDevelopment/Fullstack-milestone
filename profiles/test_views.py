from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestProfileViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Dennis")
        self.user.set_password("menace")
        self.user.save()

    def test_get_user_profile(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
