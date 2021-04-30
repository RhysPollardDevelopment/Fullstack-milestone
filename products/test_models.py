from django.test import TestCase
from products.models import Product, Company


class TestProductModels(TestCase):
    def test_product_to_string(self):
        """Tests overloaded string function"""
        product = Product.objects.create(
            name="Test product",
            description="Test description for product.",
        )
        self.assertEqual(str(product), product.name)

    def test_company_to_string(self):
        """Tests overloaded string function"""
        company = Company.objects.create(
            name="Test Company",
            description="test company description.",
            company_url="www.testsite.co.uk",
        )
        self.assertEqual(str(company), company.name)
