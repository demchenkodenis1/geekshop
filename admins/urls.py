
from django.urls import path

from admins.views import index, admin_users, admin_users_create, admin_users_update, admin_users_delete, admin_category, \
    admin_category_create, admin_category_update, admin_category_delete, admin_product, admin_product_create, \
    admin_product_update, admin_product_delete

app_name = 'admins'
urlpatterns = [
    path('', index, name='index'),
    path('users/', admin_users, name='admin_users'),
    path('users-create/', admin_users_create, name='admin_users_create'),
    path('users-update/<int:pk>', admin_users_update, name='admin_users_update'),
    path('users-delete/<int:pk>', admin_users_delete, name='admin_users_delete'),
    path('users-category/', admin_category, name='admin_category'),
    path('category-create/', admin_category_create, name='admin_category_create'),
    path('category-update/<int:pk>', admin_category_update, name='admin_category_update'),
    path('category-delete/<int:pk>', admin_category_delete, name='admin_category_delete'),
    path('users-product/', admin_product, name='admin_product'),
    path('product-create/', admin_product_create, name='admin_product_create'),
    path('product-update/<int:pk>', admin_product_update, name='admin_product_update'),
    path('product-delete/<int:pk>', admin_product_delete, name='admin_product_delete'),
]



