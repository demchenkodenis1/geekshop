from django.test import TestCase
from django.conf import settings
from django.test.client import Client

# Create your tests here.
from authapp.models import User

#TestCase
class UserManagementTestCase(TestCase):
    username = 'django'
    email = 'django@django.ru'
    password = 'geekshop'

    new_user_data = {
        'username': 'django1',
        'first_name': 'Django1',
        'last_name': 'Django2',
        'password1': 'Tsponec_2',
        'password2': 'Tsponec_2',
        'email': 'django@email.ru',
        'age': 31
    }

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    # 1 Тест Авторизация
    # Нужно проверить, что пользователь не авторизован
    def tesr_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Проверяем, что пользователь не авторизованный и является анонимным
        self.assertTrue(response.context['user'].is_anonymous)
        # Пробуем авторизоваться
        self.client.login(username=self.username, password=self.password)
        # Отправляем на авторизацию
        response = self.client.get('/users/login/')
        # Проверяем, что клиент авторизовался
        self.assertEqual(response.status_code, 302)

        # Проверяем, что клиент разлогинелся
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)

    # 2. Тест Регистрация
    def test_register(self):
        # Начинаем регистрацию
        response = self.client.post('/users/registration/', data=self.new_user_data)
        self.assertEqual(response.status_code, 302)

        # Получаем пользователя
        new_user = User.objects.get(username=self.new_user_data['username'])

        # Готовим ссылку
        activation_url = f"{settings.DOMAIN_NAME}/user/verify{self.new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 302)

        # Активируем пользователя в базе данных
        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)


    def tearDown(self) -> None:
        pass


