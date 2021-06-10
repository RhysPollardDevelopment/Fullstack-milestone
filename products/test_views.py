from django.test import TestCase
from .models import Product, Company
from .forms import ProductForm, CompanyForm
from unittest.mock import patch
from django.contrib.messages import get_messages
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from django.contrib.auth.models import User


class TestProductViews(TestCase):
    @patch("stripe.Customer.create")
    def setUp(self, mock_create):
        """
        Creates user, superuser objects for logging in along with the
        necessary recipes, products and subscriptions for required tests
        """

        # Mocks the return value for fake Customer.create function.
        mock_create.return_value = {"id": "fakeID"}

        # Create superuser for accessing add/update/delete functions.
        self.superuser = User.objects.create_superuser(
            "superuser", "superuser@test.com", password="superpassword"
        )

        # Create a product object for views to load/call.
        self.test_image = tempfile.NamedTemporaryFile(suffix="jpg").name
        self.product = Product.objects.create(
            name="Test product",
            description="Product test description",
            image=self.test_image,
        )

        # Create a company object for views to load/call.
        self.company = Company.objects.create(
            name="Test company",
            description="Company test description",
            logo=self.test_image,
            company_url="www.test.com",
        )

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

        response = self.client.get(f"/products/{self.product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")

    def test_get_partners_page(self):
        """
        Test to correctly display parter companies on a page.
        """
        response = self.client.get("/products/partners/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/partners.html")
        self.assertEqual(response.context["companies"].count(), 1)

    def test_get_add_product_page(self):

        self.client.login(username="superuser", password="superpassword")

        response = self.client.get("/products/add_product/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/add_product.html")

    def test_redirect_if_not_superuser(self):
        """
        Testing if user is redirected from a view with the decorator of
        user_pass_test(is_subscribed).
        """

        self.client.login(username="testuser", password="12345")

        response = self.client.get("/products/add_product/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_can_add_product(self):
        """
        Test that user can successfully validate and add new product.
        """

        self.client.login(username="superuser", password="superpassword")

        # which was not corrupt or invalid.
        f = BytesIO()
        image = Image.new("RGB", (100, 100))
        image.save(f, "png")
        f.seek(0)
        test_image = SimpleUploadedFile(
            "test_image.png",
            content=f.read(),
        )

        product_info = {
            "name": "Added product",
            "description": "Product Added description",
            "image": test_image,
        }

        image_data = {"image_field": test_image}

        response = self.client.post(
            "/products/add_product/",
            product_info,
        )

        form = ProductForm(product_info, files=image_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/products/product/Added%20product/")

    def test_get_update_product_page(self):
        """User can access the edit product page if superuser."""

        self.client.login(username="superuser", password="superpassword")

        response = self.client.get(
            f"/products/update_product/{self.product.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/update_product.html")

    def test_successfully_update_product_page(self):
        """User can access the edit product page if superuser."""

        self.client.login(username="superuser", password="superpassword")

        # Create image to load onto new page and avoid error.
        test_image = tempfile.NamedTemporaryFile(suffix="jpg").name

        # Updated info to save to model.
        product_info = {
            "name": "Updated product",
            "description": "Product updated description",
            "image": test_image,
        }
        image_data = {"image_field": test_image}

        # Post data to update_product.
        response = self.client.post(
            f"/products/update_product/{self.product.id}/",
            data=product_info,
            files=image_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/products/1/")

    def test_fail_to_update_product_page(self):
        """Code will alert user is form is not valid."""

        self.client.login(username="superuser", password="superpassword")

        test_image = tempfile.NamedTemporaryFile(suffix="jpg").name

        # Updated info to save to model.
        product_info = {
            "name": "updated product",
            "image": test_image,
        }

        # Post data to update_product.
        response = self.client.post(
            f"/products/update_product/{self.product.id}/",
            data=product_info,
        )
        self.assertEqual(response.status_code, 200)

        # https://stackoverflow.com/questions/2897609/how-can-i-unit-test-
        # django-messages
        # Check for error message matching invalid form.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "An error was found. Please check form is correct.",
        )

    def test_delete_product(self):
        """User can access the delete product page if superuser."""

        self.client.login(username="superuser", password="superpassword")

        delete = Product.objects.create(
            name="Deleted product",
            description="To be deleted.",
            image=self.test_image,
        )

        response = self.client.get(f"/products/delete_product/{delete.id}/")
        self.assertRedirects(response, "/products/")

        # Check if record still exists.
        existing = Product.objects.filter(pk=delete.id)
        self.assertEqual(len(existing), 0)
