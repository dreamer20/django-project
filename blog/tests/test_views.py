import os
import json
from pathlib import Path
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from project.settings import MEDIA_ROOT
from blog.models import User, Article, Profile, Category


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
        self.assertEqual('/blog/avatars/person-bounding-box.svg', user.profile.avatar.url)

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
        cls.news = Category.objects.create(name='news')
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
            'category': self.news.id
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertRedirects(response, reverse('create_article'))
        messages = list(get_messages(response.wsgi_request))
        messages = [m.message for m in messages]
        user = User.objects.get(username=self.existed_user['username'])
        self.assertEqual(user.article_set.count(), 1)
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
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('user_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/article_list.html')


class ArticleViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(cls):
        articles = Category.objects.create(name='articles')
        user = User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password'],
            email=cls.existed_user['email']
        )

        user.article_set.create(
            content='hello',
            preview='hello',
            title='some title',
            category=articles,
        )

    def test_view_url_exists_at_desired_location(self):
        article = Article.objects.all()[0]
        response = self.client.get(f'/blog/article/{article.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        article = Article.objects.all()[0]
        response = self.client.get(reverse('article', kwargs={'id': article.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        article = Article.objects.all()[0]
        response = self.client.get(reverse('article', kwargs={'id': article.id}))
        self.assertTemplateUsed(response, 'article.html')


class IndexViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(cls):
        news = Category.objects.create(name='news')
        articles = Category.objects.create(name='articles')

        user = User.objects.create_user(
            username=cls.existed_user['username'],
            password=cls.existed_user['password'],
            email=cls.existed_user['email']
        )

        user.article_set.create(
            content='hello',
            preview='hello',
            title='some title',
            category=news,
        )
        user.article_set.create(
            content='hello2',
            preview='hello2',
            title='some title',
            category=news,
        )
        user.article_set.create(
            content='hello3',
            preview='hello3',
            title='some title',
            hidden=True,
            category=articles,
        )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_view_does_not_show_hidden_articles(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context['article_list']), 2)


class AvatarViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(self):
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
        response = self.client.get('/blog/accounts/avatar/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('avatar'))
        self.assertEqual(response.status_code, 200)

    def test_view_avatar_succesfully_uploaded(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        upload_file = open(Path(MEDIA_ROOT) / 'avatars' / 'test_success.jpg', 'rb')
        data = {'avatar': SimpleUploadedFile(upload_file.name, upload_file.read())}
        response = self.client.post(reverse('avatar'), data)
        self.assertRedirects(response, reverse('avatar'))

        messages = list(get_messages(response.wsgi_request))
        messages = [m.message for m in messages]

        self.assertIn('Your avatar was successfully changed.', messages)

        user = User.objects.get(username=self.existed_user['username'])
        os.remove(user.profile.avatar.path)


class CommentsViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(self):
        articles = Category.objects.create(name='articles')
        user = User.objects.create_user(
            username=self.existed_user['username'],
            password=self.existed_user['password'],
            email=self.existed_user['email']
        )
        profile = Profile(avatar='avatars/person-bounding-box.svg', user=user)
        profile.save()
        self.article1 = user.article_set.create(
            content='hello',
            preview='hello',
            title='some title',
            category=articles,
        )
        article2 = user.article_set.create(
            content='hello2',
            preview='hello2',
            title='some title2',
            category=articles,
        )
        user.comment_set.create(
            comment='some loreum ipsum',
            username=user.username,
            article=self.article1,
            profile=user.profile
        )
        user.comment_set.create(
            comment='some loreum ipsum',
            username=user.username,
            article=self.article1,
            profile=user.profile
        )
        user.comment_set.create(
            comment='some loreum ipsum',
            username=user.username,
            article=article2,
            profile=user.profile
        )

    def test_view_returns_list_of_comments_for_article(self):
        response = self.client.get(reverse('comments', kwargs={'id': self.article1.id}))
        self.assertEqual(response.status_code, 200)
        list_of_comments = json.loads(response.json())
        self.assertEqual(len(list_of_comments), 2)

    def test_view_add_new_comment_to_article(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        data = {
            'comment': 'some comment'
        }
        response = self.client.post(
            reverse('comments', kwargs={'id': self.article1.id}),
            data)
        self.assertEqual(response.status_code, 200)
        article = Article.objects.get(pk=self.article1.id)
        self.assertEqual(article.comment_set.count(), 3)
        comment = json.loads(response.json())
        self.assertEqual(comment[0]['fields']['comment'], 'some comment')


class SearchViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(self):
        articles = Category.objects.create(name='articles')
        user = User.objects.create_user(
            username=self.existed_user['username'],
            password=self.existed_user['password'],
            email=self.existed_user['email']
        )
        user.article_set.create(
            content='hello',
            preview='hello',
            title='Hello',
            category=articles,
        )
        user.article_set.create(
            content='hello 2',
            preview='some text',
            title='some title2',
            category=articles,
        )
        user.article_set.create(
            content='my content',
            preview='my content',
            title='whats up?',
            category=articles,
        )

    def test_view_without_query_sends_to_index_page(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['article_list']), 3)

    def test_view_shows_query_results(self):
        search_url = reverse('search')
        response = self.client.get(search_url + '?q=hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['article_list']), 2)


class CategoryViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(self):
        news = Category.objects.create(name='news')
        articles = Category.objects.create(name='articles')

        user = User.objects.create_user(
            username=self.existed_user['username'],
            password=self.existed_user['password'],
            email=self.existed_user['email']
        )
        user.article_set.create(
            content='hello',
            preview='hello',
            title='Hello',
            category=news,
        )
        user.article_set.create(
            content='hello 2',
            preview='some text',
            title='some title2',
            category=news,
        )
        user.article_set.create(
            content='my content',
            preview='my content',
            title='whats up?',
            category=articles,
        )

    def test_view_shows_news_category(self):
        response = self.client.get(reverse('category', kwargs={'category': 'news'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['article_list']), 2)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_shows_article_category(self):
        response = self.client.get(reverse('category', kwargs={'category': 'articles'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['article_list']), 1)
        self.assertTemplateUsed(response, 'index.html')


class ArticleDeleteViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(self):
        news = Category.objects.create(name='news')

        user = User.objects.create_user(
            username=self.existed_user['username'],
            password=self.existed_user['password'],
            email=self.existed_user['email']
        )
        self.article = user.article_set.create(
            content='hello',
            preview='hello',
            title='Hello',
            category=news,
        )
        user.article_set.create(
            content='hello 2',
            preview='some text',
            title='some title2',
            category=news,
        )

    def test_view_redirects_unauthorized_user_on_article_deletion(self):
        delete_url = reverse('delete', kwargs={'id': self.article.id})
        response = self.client.get(delete_url)
        self.assertRedirects(response, reverse('login') + f'?next={delete_url}')

    def test_view_deletes_article(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        delete_url = reverse('delete', kwargs={'id': self.article.id})
        response = self.client.get(delete_url)
        articles = Article.objects.all()
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(articles.count(), 1)


class ArticleEditViewTest(TestCase):
    existed_user = {
        'username': 'existeduser',
        'password': 'qwerty1234',
        'email': 'test@mail.com'
    }

    @classmethod
    def setUpTestData(self):
        self.news = Category.objects.create(name='news')

        user = User.objects.create_user(
            username=self.existed_user['username'],
            password=self.existed_user['password'],
            email=self.existed_user['email']
        )
        self.article = user.article_set.create(
            content='hello',
            preview='hello',
            title='Hello',
            category=self.news,
        )

    def test_view_redirects_unauthorized_user_on_article_deletion(self):
        delete_url = reverse('edit_article', kwargs={'id': self.article.id})
        response = self.client.get(delete_url)
        self.assertRedirects(response, reverse('login') + f'?next={delete_url}')

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('edit_article', kwargs={'id': self.article.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        response = self.client.get(reverse('edit_article', kwargs={'id': self.article.id}))
        self.assertTemplateUsed(response, 'edit_article.html')

    def test_view_saves_edited_article(self):
        self.client.login(
            username=self.existed_user['username'],
            password=self.existed_user['password']
        )
        delete_url = reverse('edit_article', kwargs={'id': self.article.id})
        data = {
            'content': 'hello world',
            'preview': 'hello',
            'title': 'Hello',
            'category': self.news.id,
        }
        response = self.client.post(delete_url, data)
        self.assertRedirects(response, reverse('edit_article', kwargs={'id': self.article.id}))
        article = Article.objects.get(pk=self.article.id)
        self.assertEqual(article.content, 'hello world')
