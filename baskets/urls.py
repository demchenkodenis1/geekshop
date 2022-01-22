from django.urls import path

from baskets.views import BasketAddCreateView, basket_remove, basket_edit

app_name = 'baskets'
urlpatterns = [
    path('add/<int:id>/', BasketAddCreateView.as_view(), name='basket_add'),
    path('remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('edit/<int:id_basket>/<int:quantity>/', basket_edit, name='basket_edit')
]
