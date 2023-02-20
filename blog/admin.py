from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Article, Comment
# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(Article)
admin.site.register(Comment)
