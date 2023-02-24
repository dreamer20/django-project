from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    pass


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def natural_key(self):
        return (self.avatar.url, )


class Article(models.Model):
    title = models.CharField(max_length=300, default='Title')
    preview = tinymce_models.HTMLField(default='')
    content = tinymce_models.HTMLField(default='')
    pub_date = models.DateTimeField(default=timezone.now)
    hidden = models.BooleanField(default=False)
    tags = TaggableManager()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


class Comment(models.Model):
    comment = models.TextField(max_length=2000)
    submit_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        default=3
    )
    username = models.CharField(max_length=300)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
    )
