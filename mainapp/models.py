from django.db import models


# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(verbose_name='product_image', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=128, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.category}"
