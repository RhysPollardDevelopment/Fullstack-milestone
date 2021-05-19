from django.test import TestCase
from .models import Product
from django.core.files.uploadedfile import SimpleUploadedFile


class TestProductViews(TestCase):
    def test_get_all_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertIsNotNone(response.context["products"])

    def test_get_product_details(self):
        # Suggestion for use of simpleuploadedFile found at stack overflow.
        # https://stackoverflow.com/questions/26141786/django-1-7-imagefield
        # -form-validation?noredirect=1&lq=1
        test_image = SimpleUploadedFile(
            name="test_img.jpg",
            content=b"",
            content_type="image/jpeg",
        )
        product = Product.objects.create(
            name="Test product",
            description="Product test description",
            image=test_image,
        )
        response = self.client.get(f"/products/{product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")

    def test_get_partners_page(self):
        response = self.client.get("/products/partners/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/partners.html")
        self.assertIsNotNone(response.context["companies"])
