from django.db import models
import uuid


class Product(models.Model):
    """
    Product model contains basic information for product listings and has
    one to many relationship with producing company.
    """

    product_code = models.CharField(
        max_length=36, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    image = models.ImageField(null=True)
    texture = models.CharField(max_length=254, blank=True, null=True)
    flavour = models.CharField(max_length=254, blank=True, null=True)
    company = models.ForeignKey(
        "Company", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Company(models.Model):
    """
    Company Model has information on company which owns honey products,
    also has logo and url to would be company website.
    """

    class Meta:
        verbose_name_plural = "Companies"

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    logo = models.ImageField(null=True, blank=True)
    county = models.CharField(max_length=40, null=True, blank=True)
    company_url = models.URLField(max_length=250)

    def __str__(self):
        return self.name
