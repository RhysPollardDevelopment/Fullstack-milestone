from django.test import TestCase
from .models import Subscription

# Create your tests here.


class TestSubscriptionModel(TestCase):
        def test_subscription_to_string(self):
        """Tests overloaded string function"""
        product = Product.objects.create(
            name="Test product",
            description="Test description for product.",
        )
        self.assertEqual(str(product), product.name)