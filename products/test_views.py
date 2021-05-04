from django.test import TestCase


class TestProductViews(TestCase):
    def test_get_all_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        # Check that rendered context contains 6 products.
        self.assertEqual(len(response.context["products"]), 6)
