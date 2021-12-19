
from django.urls import path
from authapp.views import register, login, logout

app_name = 'authapp'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]



