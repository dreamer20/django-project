from django import forms
from django.forms import ValidationError
from string import ascii_letters


class RegisterForm(forms.Form):
    common_attrs = {'class': 'form-control'}

    username = forms.CharField(
        max_length=16,
        min_length=3,
        widget=forms.TextInput(attrs=common_attrs)
    )
    password = forms.CharField(
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs=common_attrs)
    )
    repeat_password = forms.CharField(
        min_length=8,
        max_length=100,
        widget=forms.PasswordInput(attrs=common_attrs)
    )

    def clean_password(self):
        password = self.cleaned_data['password']

        if any([(x in password) for x in ascii_letters]) is False:
            self.add_error('password', ValidationError('Password must contain at least one latin letter.', code='invalid'))
            # raise ValidationError('Password must contain at least one latin letter.', code='invalid')

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        # print(password, repeat_password)

        if password != repeat_password:
            self.add_error('password', ValidationError('Passwords doesn\'t match.', code='invalid'))


class LoginForm(forms.Form):
    common_attrs = {'class': 'form-control'}

    username = forms.CharField(
        widget=forms.TextInput(attrs=common_attrs)
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=common_attrs)
    )
