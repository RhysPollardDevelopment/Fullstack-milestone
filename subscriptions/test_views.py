from django.test import TestCase
from django.contrib.auth.models import User
from .models import StripeSubscription
from datetime import datetime, timezone
from unittest.mock import patch

import json


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

    @patch("stripe.Product.list")
    def test_get_subscriptions_page_when_anonymous(self, mock_product_list):
        """Test that user can access main subscription page."""
        mock_product_list.return_value = {
            "product": "test product",
            "price": "6.00",
        }
        # Assert results
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

    # https://www.obeythetestinggoat.com/book/chapter_mocking.html
    # Tutorial which made gave idea for how mock worked effectively.
    @patch("stripe.Subscription.modify")
    def test_get_cancel_subscription(self, mock_subscription_modify):
        """
        Should call cancel_subscription view and be directed to a
        confirmation page.

        If successful should also have updated cancel_at_end on subscription
        model.
        """
        # https://docs.python.org/3/library/unittest.mock.html#where-to-patch
        # Official doc which helped understand use of return_value.
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

    @patch("stripe.Customer.modify")
    @patch("stripe.Subscription.create")
    @patch("stripe.PaymentMethod.attach")
    def test_create_subscription(self, mock_attach, mock_create, mock_update):
        """
        Mocks the data sent as a post to the create-subscription view. Data is
        assigned as required and all API calls are mocked to prevent data
        creation.

        Should receive a 200 as only awaits a JsonResponse. No templates.
        """
        # Mock data and create a return value for subscription.create.
        mock_create.return_value = {"id": "test_sub_ID", "status": "active"}
        body_data = {
            "customerId": "test customer",
            "paymentMethodId": "test payment",
            "priceId": "12345",
            "sameBilling": True,
            "saveShipping": True,
            "phone_number": "+01234567",
            "street_address1": "new",
            "street_address2": "subcription",
            "town_or_city": "created",
            "county": "for",
            "postcode": "stripe",
            "full_name": "Tina Tester",
        }
        # Change data into Json format to be passed through to the view.
        # https://www.w3schools.com/python/python_json.asp
        data = json.dumps(body_data)
        self.client.login(username="testuser", password="12345")

        # https://stackoverflow.com/questions/18867898/attributeerror-str-
        # object-has-no-attribute-items
        # Stack overflow post highlighting need for content_type.

        # https://docs.djangoproject.com/en/3.2/topics/testing/tools/
        # Django doc specifying layout for post request.
        response = self.client.post(
            "/subscription/create-subscription",
            content_type="application/json",
            data=data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_update.called, True)
        self.assertEqual(mock_create.called, True)
        self.assertEqual(mock_attach.called, True)

    @patch("stripe.Customer.modify")
    @patch("stripe.Subscription.create")
    @patch("stripe.PaymentMethod.attach")
    def test_create_subscription_different_billing(
        self, mock_attach, mock_create, mock_update
    ):
        """
        Mocks the data sent as a post to the create-subscription view. Data is
        assigned as required and all API calls are mocked to prevent data
        creation.

        Should receive a 200 as only awaits a JsonResponse. No templates.
        """
        # Mock data and create a return value for subscription.create.
        mock_create.return_value = {"id": "test_sub_ID", "status": "active"}
        body_data = {
            "customerId": "test customer",
            "paymentMethodId": "test payment",
            "priceId": "12345",
            "sameBilling": False,
            "saveShipping": True,
            "phone_number": "+01234567",
            "street_address1": "new",
            "street_address2": "subcription",
            "town_or_city": "created",
            "county": "for",
            "postcode": "stripe",
            "full_name": "Tina Tester",
            "billing_full_name": "Colin Mockerie",
            "billing_town_or_city": "not same",
            "billing_address1": "different",
            "billing_address2": "other sub",
            "billing_postcode": "stripe2",
            "billing_county": "from",
            "billing_phone_number": "987654321",
        }
        # Change data into Json format to be passed through to the view.
        # https://www.w3schools.com/python/python_json.asp
        data = json.dumps(body_data)
        self.client.login(username="testuser", password="12345")

        # https://stackoverflow.com/questions/18867898/attributeerror-str-
        # object-has-no-attribute-items
        # Stack overflow post highlighting need for content_type.

        # https://docs.djangoproject.com/en/3.2/topics/testing/tools/
        # Django doc specifying layout for post request.
        response = self.client.post(
            "/subscription/create-subscription",
            content_type="application/json",
            data=data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_update.called, True)
        self.assertEqual(mock_create.called, True)
        self.assertEqual(mock_attach.called, True)
