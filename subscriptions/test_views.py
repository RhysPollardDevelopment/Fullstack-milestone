from django.test import TestCase
from django.contrib.auth.models import User
from .models import StripeSubscription
from datetime import datetime, timezone
from unittest.mock import patch


mock_subscription_object = {
    "id": "testID",
}


class TestSubscriptionViews(TestCase):
    @patch("stripe.Customer.create")
    def setUp(self, mock_create):
        mock_create.return_value = {"id": "fakeID"}
        self.user = User.objects.create(
            username="testuser",
            email="testuser@test.com",
        )
        # Need to call set_password identified at https://stackoverflow.com/
        # questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
        self.user.set_password("12345")
        self.user.save()

    # def tearDown(self):
    #     stripe.Customer.delete(self.user.userprofile.stripe_customer_id)

    def test_get_subscriptions_page_when_anonymous(self):
        """Test that user can access main subscription page."""
        # Asserts get request is successful and loads subscriptions html.
        response = self.client.get("/subscription/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "subscriptions/subscriptions_page.html"
        )
        self.assertIsNotNone(response.context["products"])

    def test_subscription_page_redirect_if_subscription_active(self):
        """
        Should redirect user if they have active subscription on specific
        views.
        """
        # Stripesubscription created to allow has_active_subscription test.
        StripeSubscription.objects.create(
            subscription_id="testsub",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )
        self.client.login(username="testuser", password="12345")

        # Asserts that client redirects to home/index page on get request.
        response = self.client.get("/subscription/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.assertTemplateNotUsed("subscriptions/subscriptions_page.html")

    @patch("stripe.Customer.retrieve")
    def test_checkout_page_get(self, mock_retrieve):
        """
        Load checkout page when accessing it.
        Assumes anonymous user as redirected if not.
        """
        # User logged in to allow access.
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/subscription/checkout")
        self.assertEqual(mock_retrieve.called, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subscriptions/checkout.html")

    def test_get_complete_page_(self):
        """
        Can call checkout/complete page when required and loads correctly.
        """
        # User logged in to allow access.
        self.client.login(username="testuser", password="12345")
        # Create data necessary for view.
        session = self.client.session
        session["save_shipping"] = True
        session["shippingdata"] = {
            "default_phone_number": "0123456",
            "default_street_address1": "street1",
            "default_street_address2": "street2",
            "default_town_or_city": "the city",
            "default_county": "a county",
            "default_postcode": "test postcode",
        }
        session.save()

        response = self.client.get("/subscription/checkout/complete")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "subscriptions/complete.html")

    @patch("stripe.Subscription.modify")
    def test_get_cancel_subscription(self, mock_subscription_modify):
        """
        Should call cancel_subscription view and be directed to a
        confirmation page.

        If successful should also have updated cancel_at_end on subscription
        model.
        """
        mock_subscription_modify.return_value = mock_subscription_object
        # Create subscription Instance and log in user.
        StripeSubscription.objects.create(
            subscription_id="testID",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
        )
        self.client.login(username="testuser", password="12345")

        response = self.client.get("/subscription/cancel_subscription/")

        self.assertEqual(mock_subscription_modify.called, True)

        # Load updated date of subscription for assertEqual
        test = StripeSubscription.objects.get(
            subscription_id=mock_subscription_object["id"]
        )

        self.assertEqual(test.cancel_at_end, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "subscriptions/cancel_confirmation.html"
        )

    @patch("stripe.Subscription.modify")
    def test_get_renew_subscription(self, mock_update):
        """
        Should call cancel_subscription view and be directed to a
        confirmation page.
        """
        # Define mocked function's return value.
        mock_update.return_value = mock_subscription_object

        # Create subscription Instance and log in user.
        StripeSubscription.objects.create(
            subscription_id="testID",
            start_date=datetime(2020, 5, 5, 12, 0, 0, tzinfo=timezone.utc),
            end_date=datetime(2030, 6, 5, 12, 0, 0, tzinfo=timezone.utc),
            stripe_user=self.user.userprofile,
            cancel_at_end=True,
        )
        self.client.login(username="testuser", password="12345")

        # Assert results
        response = self.client.get("/subscription/reactivate/")

        # Load updated date of subscription for assertEqual
        test_renew = StripeSubscription.objects.get(
            subscription_id=mock_subscription_object["id"]
        )

        self.assertEqual(mock_update.called, True)
        self.assertEqual(test_renew.cancel_at_end, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "subscriptions/reactivate_confirmation.html"
        )
