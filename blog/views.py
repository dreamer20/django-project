from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.forms import ValidationError
from .forms import RegisterForm, LoginForm
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'user': request.user})
    return render(request, 'index.html')


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data['username'])
            except User.DoesNotExist:
                User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
            else:
                form.add_error('username', ValidationError('Username already exist.', code='invalid'))
                return render(request, self.template_name, {'form': form})
            messages.success(request, 'Registrations is succesfull. Now you can log in.')
            return HttpResponseRedirect(reverse('login'))

        else:
            return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(
            request, self.template_name,
            {
                'form': form,
                'registration_status': request.GET.get('registration_status')
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')

            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Invalid password or username')
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))
