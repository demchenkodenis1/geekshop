# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.db.migrations import Migration

from authapp.models import User
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Формируется'),
        (SEND_TO_PROCEED, 'Отправлен в обработку'),
        (PAID, 'Оплачено'),
        (PROCEEDED, 'В обработке'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отмена заказа')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='Статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='Активный', db_index=True, default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_values(self):
        return self.orderitems.select_related()

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'get_total_cost': sum(list(map(lambda x: x.get_product_cost(), items))),
            'get_total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
