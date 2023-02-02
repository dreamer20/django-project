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
        self.assertTrue(form.fields['password'].label is None
                        or form.fields['password'].label == 'password')

    def test_password_min_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password'].min_length, 8)

    def test_password_max_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password'].max_length, 100)

    def test_repeat_password_form_field_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['repeat_password'].label is None
                        or form.fields['repeat_password'].label == 'repeat_password')

    def test_repeat_password_min_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['repeat_password'].min_length, 8)

    def test_repeat_password_max_length(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password'].max_length, 100)

    def test_password_math(self):
        """
        Validation return False if password and repeat_password fields isn't equal
        and has error string.
        """
        data = {
            'password': 'qwerty1234',
            'repeat_password': '1234qwerty'
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords doesn\'t match.', form.errors['password'])

    def test_password_validity(self):
        """
        Validation return False if password don't have at least one latin letter.
        """
        data = {
            'password': '12345678',
            'repeat_password': '12345678'
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Password must contain at least one latin letter.', form.errors['password'])


class LoginFormTest(TestCase):
    def test_username_form_field_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['username'].label is None
                        or form.fields['username'].label == 'username')

    def test_password_form_field_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['password'].label is None
                        or form.fields['password'].label == 'password')
