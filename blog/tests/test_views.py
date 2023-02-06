from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password'],
            email=cls.existed_user['email']
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/accounts/registration/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_view_create_user(self):
        newusername = 'brandnewuser'
        data = {
            'username': newusername,
            'password1': 'peri54ir7end',
            'password2': 'peri54ir7end',
            'email': 'gv4alex@gmail.com',
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('django_registration_complete'))
        user = User.objects.get(username=newusername)
        self.assertEqual(newusername, user.username)

    def test_view_redirects_to_index_page_if_authorized(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('index'))


class RegisterCompleteViewTest(TestCase):
    def test_view_shows_404_if_registration_not_performed(self):
        response = self.client.get('/blog/accounts/registration/complete/')
        self.assertEqual(response.status_code, 404)


class ActivationCompleteViewTest(TestCase):
    def test_view_shows_404_if_activation_not_performed(self):
        response = self.client.get('/blog/accounts/activation/complete/')
        self.assertEqual(response.status_code, 404)


class LoginViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password'],
            email=cls.existed_user['email']
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

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
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_view_redirects_to_index_page_if_authorized(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('index'))


class LogoutViewTest(TestCase):
    def test_view_redirects_correctly_after_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))


class PasswordResetViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password'],
            email=cls.existed_user['email']
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_view_redirect_after_sending_email(self):
        data = {
            'email': self.existed_user['email'],
        }
        response = self.client.post(reverse('password_reset'), data)
        self.assertRedirects(response, reverse('password_reset_done'))


class PasswordResetDoneViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')


class PasswordResetCompleteViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_complete.html')


class PasswordResetConfirmViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password'],
            email=cls.existed_user['email']
        )
