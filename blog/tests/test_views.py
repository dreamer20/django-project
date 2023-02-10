from django.test import TestCase
from django.urls import reverse
from blog.models import User
from django.contrib.messages import get_messages


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


class ProfileViewTest(TestCase):
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

    def test_view_redirects_to_login_view_if_not_authenticated(self):
        profile_url = reverse('profile')
        login_url = reverse('login')
        response = self.client.get(profile_url)
        self.assertRedirects(response, f'{login_url}?next={profile_url}')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get('/blog/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)


class PasswordChangeViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    def setUp(self):
        User.objects.create_user(
            username=self.existed_user['username'],
            password=self.existed_user['password'],
            email=self.existed_user['email']
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get('/blog/accounts/password_change/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_view_template_has_password_change_success_message(self):
        data = {
            'old_password': 'qwerty1234',
            'new_password1': 'peri54ri7end',
            'new_password2': 'peri54ri7end',
        }
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.post(reverse('password_change'), data=data)
        messages = list(get_messages(response.wsgi_request))
        messages = [m.message for m in messages]
        self.assertIn('Your password was successfully changed.', messages)


class EmailChangeViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    def setUp(self):
        User.objects.create_user(
            username=self.existed_user['username'],
            password=self.existed_user['password'],
            email=self.existed_user['email']
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get('/blog/accounts/email_change/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('email_change'))
        self.assertEqual(response.status_code, 200)

    def test_view_template_has_email_change_success_message(self):
        data = {
            'new_email': 'newtest@gmail.com',
        }
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.post(reverse('email_change'), data=data)
        messages = list(get_messages(response.wsgi_request))
        messages = [m.message for m in messages]
        self.assertIn('Your email was successfully changed.', messages)


class CreateArticleViewTest(TestCase):
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

    def test_view_redirects_to_login_view_if_not_authenticated(self):
        profile_url = reverse('create_article')
        login_url = reverse('login')
        response = self.client.get(profile_url)
        self.assertRedirects(response, f'{login_url}?next={profile_url}')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get('/blog/article/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 200)

    def test_view_create_article(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        data = {
            'title': 'hello',
            'content': 'hello',
            'preview': 'hello',
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertRedirects(response, reverse('create_article'))
        messages = list(get_messages(response.wsgi_request))
        messages = [m.message for m in messages]
        user = User.objects.get(username=self.existed_user['username'])
        self.assertEqual(len(user.article_set.all()), 1)
        self.assertIn('Article created', messages)


class UserArticleListTest(TestCase):
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

    def test_view_redirects_to_login_view_if_not_authenticated(self):
        user_articles_url = reverse('user_articles')
        login_url = reverse('login')
        response = self.client.get(user_articles_url)
        self.assertRedirects(response, f'{login_url}?next={user_articles_url}')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get('/blog/accounts/articles/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('user_articles'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/article_list.html')
