from django.db import models


class Product(models.Model):
    """Data model for products."""
    product_name = models.CharField(max_length=100)
    product_brand = models.CharField(max_length=50)
    product_description = models.TextField(max_length=1000)
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    product_image = models.URLField()

    def __repr__(self):
        return self.product_name

