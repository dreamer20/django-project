from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth import forms as authForms
from django_registration.forms import RegistrationForm
from django.core.validators import EmailValidator
from .models import User


class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
    common_attrs = {'class': 'form-control'}

    username = forms.CharField(
        max_length=16,
        min_length=3,
        widget=forms.TextInput(attrs=common_attrs)
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=common_attrs)
    )
    password1 = forms.CharField(
        label='Password',
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs=common_attrs)
    )
    password2 = forms.CharField(
        label='Repeat password',
        min_length=8,
        max_length=100,
        widget=forms.PasswordInput(attrs=common_attrs)
    )


class LoginForm(authForms.AuthenticationForm):
    common_attrs = {'class': 'form-control'}

    username = forms.CharField(
        widget=forms.TextInput(attrs=common_attrs)
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=common_attrs)
    )


class PasswordResetForm(authForms.PasswordResetForm):
    common_attrs = {'class': 'form-control'}

    email = forms.EmailField(
        widget=forms.EmailInput(attrs=common_attrs)
    )


class SetPasswordForm(authForms.SetPasswordForm):
    common_attrs = {'class': 'form-control', "autocomplete": "new-password"}

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(common_attrs),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(common_attrs),
    )


class PasswordChangeForm(authForms.PasswordChangeForm):
    common_attrs = {'class': 'form-control'}

    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(common_attrs),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(common_attrs),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(common_attrs),
    )


class EmailForm(forms.Form):
    common_attrs = {'class': 'form-control'}

    new_email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(common_attrs),
        validators=[EmailValidator]
    )
