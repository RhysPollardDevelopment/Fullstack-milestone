import re
from django.test import TestCase


class TestSubscriptionViews(TestCase):
    def test_get_subscriptions_page(self):
        """Test that user can access main subscription page."""
        response = self.client.get("/subscription/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "subscriptions/subscriptions_page.html"
        )
        self.assertIsNotNone(response.context["products"])
