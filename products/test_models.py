from django.test import TestCase
from products.models import Product, Company


class TestProductModels(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            description="test company description.",
            county="Cornwall",
            company_url="www.testsite.co.uk",
        )
        self.product = Product.objects.create(
            name="Test product",
            description="Test description for product.",
            texture="honey like",
            flavour="honey flavoured",
            company=self.company,
        )

    def test_product_creation(self):
        product = self.product
        self.assertTrue(isinstance(product, Company))
