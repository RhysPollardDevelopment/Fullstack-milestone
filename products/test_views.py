from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Product, Company
from unittest.mock import patch
from django.contrib.messages import get_messages
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from django.conf import settings
import shutil

from recipes.models import Recipe
from django.contrib.auth.models import User

# New images are created in a tempfolder for deletion.
settings.MEDIA_ROOT = tempfile.mkdtemp()


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

        # Creates enough products to satisfy page requirements.
        i = 1
        while i < 5:
            Product.objects.create(
                name=f"new product{i}",
                description=f"Product test description {i}",
                image=self.test_image,
            )
            Recipe.objects.create(
                title=f"New recipe {i}",
                description=f"New recipe description {i}",
                image=self.test_image,
                publish_date=datetime(
                    2021, i, 1, 10, 40, 30, 0, tzinfo=timezone.utc
                ),
            )
            i += 1

    def tearDown(self):
        """Clears temp folder after tests"""
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

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

        products = response.context["products"]
        recipes = response.context["recipes"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertEqual(len(products), 4)
        self.assertEqual(len(recipes), 2)

    def test_get_add_product_page(self):
        """Can successfully ass a product using product form"""

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

        response = self.client.post(
            "/products/add_product/",
            product_info,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/products/6/")

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


class TestCompanyViews(TestCase):
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

    def tearDown(self):
        """Clears temp folder after tests"""
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_get_partners_page(self):
        """
        Test to correctly display parter companies on a page.
        """
        response = self.client.get("/products/partners/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/partners.html")
        self.assertEqual(response.context["companies"].count(), 1)

    def test_get_add_company_page(self):

        self.client.login(username="superuser", password="superpassword")

        response = self.client.get("/products/partners/add_company/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/add_company.html")

    def test_redirect_if_not_superuser(self):
        """
        Testing if user is redirected from a view with the decorator of
        user_pass_test(is_subscribed).
        """

        self.client.login(username="testuser", password="12345")

        response = self.client.get("/products/partners/add_company/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_can_add_company(self):
        """
        Test that user can successfully validate and add new company.
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

        company_info = {
            "name": "Added company",
            "description": "company Added description",
            "logo": test_image,
            "company_url": "www.newcompany.com",
        }

        response = self.client.post(
            "/products/partners/add_company/",
            company_info,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/products/partners/")

    def test_get_update_company_page(self):
        """User can access the edit company page if superuser."""

        self.client.login(username="superuser", password="superpassword")

        response = self.client.get(
            f"/products/partners/update_company/{self.company.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/update_company.html")

    def test_successfully_update_company_page(self):
        """User can access the edit company page if superuser."""

        self.client.login(username="superuser", password="superpassword")

        # Create image to load onto new page and avoid error.
        test_image = tempfile.NamedTemporaryFile(suffix="jpg").name

        # Updated info to save to model.
        company_info = {
            "name": "Updated product",
            "description": "Product updated description",
            "logo": test_image,
            "company_url": "www.update.com",
        }
        image_data = {"image_field": test_image}

        # Post data to update_company.
        response = self.client.post(
            f"/products/partners/update_company/{self.company.id}/",
            data=company_info,
            files=image_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/products/partners/")

    def test_fail_to_update_company_page(self):
        """Code will alert user is form is not valid."""

        self.client.login(username="superuser", password="superpassword")

        test_image = tempfile.NamedTemporaryFile(suffix="jpg").name

        # Updated info to save to model.
        company_info = {
            "name": "updated company",
            "image": test_image,
        }

        # Post data to update_company.
        response = self.client.post(
            f"/products/partners/update_company/{self.company.id}/",
            data=company_info,
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

    def test_delete_company(self):
        """User can access the delete company page if superuser."""

        self.client.login(username="superuser", password="superpassword")

        delete = Company.objects.create(
            name="Deleted company",
            description="To be deleted.",
            logo=self.test_image,
        )

        response = self.client.get(
            f"/products/partners/delete_company/{delete.id}/"
        )
        self.assertRedirects(response, "/products/partners/")

        # Check if record still exists.
        existing = Company.objects.filter(pk=delete.id)
        self.assertEqual(len(existing), 0)
