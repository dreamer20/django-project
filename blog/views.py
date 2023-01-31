from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from .forms import RegisterForm
# Create your views here.


def index(request):
    return HttpResponse('This is my blog')


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})
