from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class RegisterViewTest(TestCase):
    existed_username = 'existeduser'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=cls.existed_username, password='qwerty1234')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_view_create_user(self):
        newusername = 'brandnewuser'
        data = {
            'username': newusername,
            'password': 'qwerty1234',
            'repeat_password': 'qwerty1234'
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('login'))
        messages = [str(m) for m in list(get_messages(response.wsgi_request))]
        self.assertIn('Registrations is succesfull. Now you can log in.', messages)
        user = User.objects.get(username=newusername)
        self.assertEqual(newusername, user.username)

    def test_view_return_user_already_exist_form_error(self):
        data = {
            'username': self.existed_username,
            'password': 'qwerty1234',
            'repeat_password': 'qwerty1234'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'Username already exist.')


class LoginViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234'
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password']
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_view_authenticate_user(self):
        data = {
            'username': self.existed_user['username'],
            'password': self.existed_user['password']
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertRedirects(response, reverse('index'))

    def test_view_authorization_fail(self):
        data = {
            'username': 'nonexisteduser',
            'password': 'qwertyqwerty'
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, 200)
        messages = [str(m) for m in list(response.context['messages'])]
        self.assertIn('Invalid password or username', messages)


class IndexViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234'
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password']
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_index_page_has_logged_user_info(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )

        response = self.client.get(reverse('index'))
        self.assertIn('user', response.context)
        self.assertEqual(self.existed_user['username'], response.context['user'].username)


class LogoutViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234'
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password']
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/logout/')
        self.assertRedirects(response, reverse('index'))

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))

    def test_user_logged_out_after_logout(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertNotIn(self.existed_user['username'].encode('utf8'), response.content)
