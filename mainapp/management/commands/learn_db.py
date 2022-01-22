from django.core.management.base import BaseCommand
from mainapp.models import Product
from django.db.models import Q


class Commnad(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.filter(
            # ~Q(category__name='Обувь')
            # Q(category__name='Обувь')
            Q(category__name='Обувь') | Q(category__name='Одежда')
        )
        print(products)
