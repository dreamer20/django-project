from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('accounts/registration/', views.RegisterView.as_view(), name='register'),
    path('accounts/registration/complete/', views.RegisterCompleteView.as_view(), name='django_registration_complete'),
    path('accounts/activation/complete/', views.ActivationCompleteView.as_view(), name='django_registration_activation_complete'),
    path('accounts/activation/<str:activation_key>/', views.ActivationView.as_view(), name='django_registration_activate'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/email_change/', views.EmailChangeView.as_view(), name='email_change'),
    path('accounts/articles/', views.UserArticleList.as_view(), name='user_articles'),
    path('accounts/avatar/', views.AvatarView.as_view(), name='avatar'),
    path('article/create/', views.CreateArticleView.as_view(), name='create_article'),
    path('article/<int:id>/', views.ArticleView.as_view(), name='article'),
    path('article/<int:id>/show/', views.ArticleShowView.as_view(), name='show_article'),
    path('article/<int:id>/hide/', views.ArticleHideView.as_view(), name='hide_article'),
    path('article/<int:id>/comments/', views.CommentsView.as_view(), name='comments'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<str:category>', views.CategoryView.as_view(), name='category'),
]
