from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from authapp.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm
from authapp.models import User
from mainapp.mixin import BaseClassContextMixin, UserDipatchMixin


class UserLoginView(LoginView, BaseClassContextMixin):
    model = User
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    title = 'geekshop | Авторизация'
    success_url = reverse_lazy('mainapp:products')

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect(self.success_url)
    #     return HttpResponseRedirect(reverse('authapp:login'))


class UserShopCreateView(CreateView, BaseClassContextMixin):
    model = User
    template_name = 'authapp/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('authapp:login')
    title = 'geekshop | Создать пользователя'

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались!')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке.'
        message = f'Для потверждения учетной записи {user.username} на портале: \n' \
                  f'{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email: str, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
                return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))


class UserShopUpdateView(UpdateView, BaseClassContextMixin, UserDipatchMixin):
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    title = 'geekshop - Профиль'

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return redirect(self.success_url)

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, "Вы успешно зарегистрировались")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(UserShopUpdateView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

class UserLogoutView(LogoutView, BaseClassContextMixin):
    template_name = 'mainapp/index.html'
    title = 'geekshop | Выход'
