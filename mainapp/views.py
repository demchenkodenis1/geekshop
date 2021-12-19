from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

import json
import os

from django.views.generic import DetailView

from mainapp.models import Product, ProductCategory

MODULE_DIR = os.path.dirname(__file__)


# Create your views here.

def index(request):
    context = {
        'title': 'Geekshop'}
    return render(request, 'mainapp/index.html', context)


def products(request, id_category=None, page=1):

    context = {'title': 'Geekshop - Товары',
               'categories': ProductCategory.objects.all(),
               }
    if id_category:
        products = Product.objects.filter(category_id=id_category)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator

    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    """ КОнтроллер вывода информации о продукте"""
    model = Product
    template_name = 'mainapp/detail.html'
    # context_object_name = 'product'

    # def get_context_data(self, **kwargs):
    #     """" Добавляем список категорий для вывода сайтбара с категориями на странице каталога"""
    #     context = super(ProductDetail, self).get_context_data(**kwargs)
    #     product = self.get_object()
    #     context['product'] = product
    #     return context

