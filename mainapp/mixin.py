from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin


class CustomDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CustomDispatchMixin, self).dispatch(request, *args, **kwargs)
    
    
class BaseClassContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class UserDipatchMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDipatchMixin, self).dispatch(request, *args, **kwargs)


class MaxSizeValidator(MaxValueValidator):
    message = _('The file exceed the maximum size of %(limit_value)s MB.')

    def __call__(self, value):
        # get the file size as cleaned value
        cleaned = self.clean(value.size)
        params = {'limit_value': self.limit_value, 'show_value': cleaned, 'value': value}
        if self.compare(cleaned, self.limit_value * 1024 * 1024): # convert limit_value from MB to Bytes
            raise ValidationError(self.message, code=self.code, params=params)

