from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.conf import settings
from django.core.cache import cache

from .mixin import BaseClassContextMixin
from .models import ProductCategory, Product


# Create your views here.


class IndexTemplateView(TemplateView, BaseClassContextMixin):
    template_name = 'mainapp/index.html'
    title = 'geekshop'


class CatalogListView(ListView, BaseClassContextMixin):
    model = Product
    template_name = 'mainapp/products.html'
    title = 'geekshop | Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)

        context['categories'] = get_link_category()
        if self.kwargs:
            products = Product.objects.filter(category_id=self.kwargs.get('id_category')).select_related('category')
        else:
            products = Product.objects.all().select_related('category')
        paginator = Paginator(products, per_page=6)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['products'] = page_obj
        return context


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        """Добавляем список категории для вывода сайдбара с катеногриями на странице каталога"""
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['product'] = get_product(self.kwargs['pk'])
        return context


def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, id=pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(id=pk)


