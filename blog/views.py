from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django_registration.backends.activation import views as reg_views
from django_registration.exceptions import ActivationError
from django_registration import signals
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.forms import ValidationError
from .forms import RegisterForm, LoginForm, PasswordResetForm, SetPasswordForm
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'user': request.user})
    return render(request, 'index.html')


class RegisterView(reg_views.RegistrationView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    email_subject_template = 'email/activation_email_subject.txt'

    def form_valid(self, form):
        success_url = self.get_success_url(self.register(form))
        self.request.session['was_registered'] = True
        self.request.session['email'] = form.cleaned_data['email']
        return HttpResponseRedirect(success_url)

    def send_activation_email(self, user):
        """
        Custom method to enable HTML activation emails.
        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context['user'] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = ''.join(subject.splitlines())
        text_content = render_to_string(
            template_name='email/activation_email_body.txt',
            context=context,
            request=self.request
        )
        html_content = render_to_string(
            template_name='email/activation_email_body.html',
            context=context,
            request=self.request
        )
        send_mail(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request, self.template_name)


class RegisterCompleteView(TemplateView):
    template_name = 'accounts/registration_complete.html'

    def get(self, request, *args, **kwargs):
        was_registered = request.session.get('was_registered')
        if was_registered:
            email = request.session.get('email')
            return render(request, self.template_name, {'email': email})
        raise Http404


class ActivationView(reg_views.ActivationView):
    template_name = 'accounts/activation_fail.html'

    def get(self, *args, **kwargs):
        extra_context = {}
        try:
            activated_user = self.activate(*args, **kwargs)
        except ActivationError as e:
            extra_context["activation_error"] = {
                "message": e.message,
                "code": e.code,
                "params": e.params,
            }
        else:
            signals.user_activated.send(
                sender=self.__class__, user=activated_user, request=self.request
            )
            self.request.session['was_activated'] = True
            return HttpResponseRedirect(force_str(self.get_success_url(activated_user)))
        context_data = self.get_context_data()
        context_data.update(extra_context)
        return self.render_to_response(context_data)


class ActivationCompleteView(TemplateView):
    template_name = 'accounts/activation_complete.html'

    def get(self, request, *args, **kwargs):
        was_registered = request.session.get('was_activated')
        if was_registered:
            return render(request, self.template_name)
        raise Http404


class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    next_page = '/blog/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request, self.template_name)


class PasswordResetView(views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'accounts/password_reset.html'
    success_url = '/blog/accounts/password_reset/done/'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class LogoutView(views.LogoutView):
    next_page = '/blog/'
