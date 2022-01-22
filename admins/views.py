from collections import OrderedDict

from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdminRegistrationForm, \
    ProductAdminProfileForm, CategoryUpdateFormAdmin
from authapp.models import User
from mainapp.mixin import CustomDispatchMixin, BaseClassContextMixin
from mainapp.models import Product, ProductCategory
from ordersapp.models import Order


class UserTemplateView(TemplateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin.html'


class UserListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    title = 'Админ | Пользователи'


class UserCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админ | Создать пользователя'


class UserUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админ | Редактирование пользователя'


class UserDeleteView(DeleteView, CustomDispatchMixin, BaseClassContextMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админ | Удаление пользователя'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = 'admins/products/admin-products-read.html'
    title = 'Админ | Продукты'


class ProductCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin, SuccessMessageMixin):
    model = Product
    template_name = 'admins/products/admin-products-create.html'
    form_class = ProductAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_products')
    success_message = "%(name)s продукт успешно создан"
    title = 'Админ | Создать продукт'

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, "Продукт успешно создан!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ProductUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = 'admins/products/admin-products-update-delete.html'
    form_class = ProductAdminProfileForm
    success_url = reverse_lazy('admins:admin_products')
    title = 'Админ | Редактирование товар'


class ProductDeleteView(DeleteView, CustomDispatchMixin, BaseClassContextMixin):
    model = Product
    template_name = 'admins/products/admin-products-update-delete.html'
    success_url = reverse_lazy('admins:admin_products')
    title = 'Админ | Удаление товара'


class CategoriesListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-read.html'
    title = 'Админ | Категории'


class CategoriesCreateView(CreateView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-create.html'
    form_class = CategoryUpdateFormAdmin
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админ | Создать категорию'

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, "Категория успешна создана!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class CategoriesUpdateView(UpdateView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-update.html'
    form_class = CategoryUpdateFormAdmin
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админ | Редактирование категории'

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
        return HttpResponseRedirect(self.get_success_url())


class CategoriesDeleteView(DeleteView, CustomDispatchMixin, BaseClassContextMixin):
    model = ProductCategory
    template_name = 'admins/categories/admin-categories-read.html'
    success_url = reverse_lazy('admins:admin_categories')
    title = 'Админ | Удаление категории'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.product_set.update(is_active=False)
            self.object.is_active = False
        else:
            self.object.product_set.update(is_active=True)
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class OrdersListView(ListView, CustomDispatchMixin, BaseClassContextMixin):
    model = Order
    template_name = 'admins/orders/admin-orders-read.html'
    title = 'Админ | Заказы'



def order_change_status(request, pk):
    statuses = ['FM', 'STP', 'PD', 'PRD', 'RDY', 'CNC']
    element = Order.objects.get(id=pk)
    element.status = statuses[(statuses.index(element.status) + 1) % len(statuses)]
    element.save()

    return HttpResponseRedirect(reverse('admins:admin_orders'))




