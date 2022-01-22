import json
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import User

def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)

class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('mainapp/fixtures/category.json')

        ProductCategory.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductCategory(**cat)
            new_category.save()

        products = load_from_json('mainapp/fixtures/products.json')

        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            prod['id'] = product.get('pk')
            category = prod.get('category')
            _category = ProductCategory.objects.get(id=category)
            prod['category'] = _category
            new_category = Product(**prod)
            new_category.save()

        User.objects.all().delete()
        User.objects.create_superuser('uegene', 'uegene@mail.ru', '1')