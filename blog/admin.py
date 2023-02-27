from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Article, Comment, Category


admin.site.register(User, UserAdmin)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)
