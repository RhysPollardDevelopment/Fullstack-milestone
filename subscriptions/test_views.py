from django.test import TestCase
from django.contrib.auth.models import User
from .models import StripeSubscription
from datetime import datetime, timezone


class TestSubscriptionViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="testuser@test.com",
        )
        # Need to call set_password identified at https://stackoverflow.com/
        # questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.user.set_password("12345")
        self.user.save()

    def test_get_subscriptions_page_when_anonymous(self):
        """Test that user can access main subscription page."""
        response = self.client.get("/subscription/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "subscriptions/subscriptions_page.html"
        )
        self.assertIsNotNone(response.context["products"])

    def test_subscription_page_redirect_if_subscription_active(self):
        """Should redirect user if they have active subscription."""
        StripeSubscription.objects.create(
            subscription_id="testsub",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/subscription/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.assertTemplateNotUsed("subscriptions/subscriptions_page.html")
