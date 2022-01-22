from django.core.management.base import BaseCommand
from prettytable import PrettyTable

from ordersapp.models import OrderItem
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from datetime import timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):
        OBJECT_1 = 1
        OBJECT_2 = 2
        OBJECT_EXPIRED = 3

        object_1__time_delta = timedelta(hours=12)
        object_2__time_delta = timedelta(days=1)

        object_1__discount = 0.3
        object_2__discount = 0.15
        object_expired__discount = 0.05

        object_1__condition = Q(order__updated__lte=F('order__created') + object_1__time_delta)

        object_2__condition = Q(order__updated__gt=F('order__created') + object_1__time_delta) & \
            Q(order__updated__lte=F('order__created') + object_2__time_delta)

        object_expired__condition = Q(order__updated__gt=F('order__created') + object_2__time_delta)

        object_1__order = When(object_1__condition, then=OBJECT_1)
        object_2__order = When(object_2__condition, then=OBJECT_2)
        object_expired__order = When(object_expired__condition, then=OBJECT_EXPIRED)

        object_1__price = When(object_1__condition,
                               then=F('product__price') * F('quantity') * object_1__discount)
        object_2__price = When(object_2__condition,
                               then=F('product__price') * F('quantity') * -object_2__discount)
        object_expired__price = When(object_expired__condition,
                                     then=F('product__price') * F('quantity') * object_expired__discount)

        test_orderss = OrderItem.objects.annotate(
            object_order=Case(
                object_1__order,
                object_2__order,
                object_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                object_1__price,
                object_2__price,
                object_expired__price,
                output_field=DecimalField(),
            )).order_by('object_order', 'total_price').select_related()

        t_list = PrettyTable(["Заказ", "Товар", "Скидка", "Разница времени"])
        t_list.align = 'l'
        for orderitem in test_orderss:
            t_list.add_row([f'{orderitem.object_order} заказ №{orderitem.pk:}', f'{orderitem.product.name}',
                            f'{abs(orderitem.total_price):6.2f} руб.',
                            orderitem.order.updated - orderitem.order.created])

        print(t_list)
