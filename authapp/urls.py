from django.urls import path
from authapp.views import UserLoginView, UserShopCreateView, UserLogoutView, UserShopUpdateView

app_name = 'authapp'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserShopCreateView.as_view(), name='registration'),
    path('profile/', UserShopUpdateView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('verify/<str:email>/<str:activate_key>/', UserShopCreateView.verify, name='verify')
]
