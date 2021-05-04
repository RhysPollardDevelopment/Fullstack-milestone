from django.test import TestCase
from .models import Product, Company


class TestProductViews(TestCase):
    def test_get_all_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        # Check that rendered context contains 6 products.
        self.assertEqual(len(response.context["products"]), 6)

    def test_get_product_details(self):
        product = Product.objects.create(
            name="Test product",
            description="Product test description",
        )
        response = self.client.get(f"/products/{product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
