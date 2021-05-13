from django.test import TestCase
from .models import Product


class TestProductViews(TestCase):
    def test_get_all_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertIsNotNone(response.context["products"])

    def test_get_product_details(self):
        product = Product.objects.create(
            name="Test product",
            description="Product test description",
        )
        response = self.client.get(f"/products/{product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")

    def test_get_partners_page(self):
        response = self.client.get("/products/partners/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/partners.html")
        self.assertIsNotNone(response.context["companies"])
