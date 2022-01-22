from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.db import models
from authapp.models import MaxSizeValidator


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активный', db_index=True, default=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='product_image', validators=[MaxSizeValidator(2)])
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Активный', db_index=True, default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']