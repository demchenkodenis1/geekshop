from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from baskets.models import Basket
from mainapp.models import Product


def basket_add(request, id):
    user_select = request.user
    product = Product.objects.get(id=id)
    baskets = Basket.objects.filter(user=user_select, product=product)

    if baskets:
        basket = baskets.first()
        basket.quantity +=1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        Basket.objects.create(user=user_select, product=product, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # Остаемся на том же шаблоне


def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
