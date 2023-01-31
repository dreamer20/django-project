from django import forms


class RegisterForm(forms.Form):
    common_attrs = {'class': 'form-control'}

    username = forms.CharField(
        max_length=20,
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

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['repeat_password']:
            self.errors['password'] = ['Password do not match.']
            del form_data['password']
        return form_data
