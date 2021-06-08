from django.test import TestCase
from .models import Product
import tempfile


class TestProductViews(TestCase):
    def test_get_all_products(self):
        """
        Test to get the main products page.
        """
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertIsNotNone(response.context["products"])

    def test_get_product_details(self):
        """
        Test to correctly retrieve a products details and display page.
        """
        test_image = tempfile.NamedTemporaryFile(suffix="jpg").name
        product = Product.objects.create(
            name="Test product",
            description="Product test description",
            image=test_image,
        )
        response = self.client.get(f"/products/{product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")

    def test_get_partners_page(self):
        """
        Test to correctly display parter companies on a page.
        """
        response = self.client.get("/products/partners/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/partners.html")
        self.assertIsNotNone(response.context["companies"])
