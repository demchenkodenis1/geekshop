from django.contrib import admin

# Register your models here.
from authapp.models import User

admin.site.register(User)
