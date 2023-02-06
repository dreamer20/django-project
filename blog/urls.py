from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
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
    # path('accounts/', include('django_registration.backends.activation.urls')),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
]
