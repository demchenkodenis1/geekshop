from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from mainapp.mixin import MaxSizeValidator, BaseClassContextMixin


class User(AbstractUser, BaseClassContextMixin):
    image = models.ImageField(verbose_name='Аватар', upload_to='users_image',
        blank=True, validators=[MaxSizeValidator(2)])
    age = models.PositiveIntegerField(verbose_name='Возраст', default=18)
    email = models.EmailField(max_length=255, unique=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires + timedelta(hours=48):
            return False
        return True


class UserProfile(models.Model):
    MALE = 'M'
    FAMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FAMALE, 'Ж'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, blank=True, max_length=2)
    langs = models.CharField(verbose_name='Язык', blank=True, max_length=10, default='Русский')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()