from django.test import TestCase
from blog.forms import RegisterForm, LoginForm


class RegistrationFormTest(TestCase):
    def test_username_form_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['username'].label is None
                        or form.fields['username'].label == 'username')

    def test_username_min_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['username'].min_length, 3)

    def test_username_max_lenth(self):
        form = RegisterForm()
        self.assertEqual(form.fields['username'].max_length, 16)

    def test_password_form_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['password1'].label is None
                        or form.fields['password1'].label == 'Password')

    def test_password1_min_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password1'].min_length, 8)

    def test_password1_max_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password1'].max_length, 100)

    def test_password2_form_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['password2'].label is None
                        or form.fields['password2'].label == 'Repeat password')

    def test_password2_min_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password2'].min_length, 8)

    def test_password2_max_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password2'].max_length, 100)


class LoginFormTest(TestCase):
    def test_username_form_field_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['username'].label is None
                        or form.fields['username'].label == 'Username')

    def test_password_form_field_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['password'].label is None
                        or form.fields['password'].label == 'password')
