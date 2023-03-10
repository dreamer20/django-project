import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views, update_session_auth_hash
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core import serializers
from django.utils.encoding import force_str
from django_registration.backends.activation import views as reg_views
from django_registration.exceptions import ActivationError
from django_registration import signals
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from . import forms
from .models import Article, Profile, Comment, Category


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(hidden=False).order_by('-pub_date')


class CategoryView(ListView):
    template_name = 'index.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs['category'])
        return Article.objects.filter(hidden=False, category=category).order_by('-pub_date')


class RegisterView(reg_views.RegistrationView):
    form_class = forms.RegisterForm
    template_name = 'accounts/register.html'
    email_subject_template = 'email/activation_email_subject.txt'

    def form_valid(self, form):
        new_user = self.register(form)
        profile = Profile(avatar='avatars/person-bounding-box.svg', user=new_user)
        profile.save()
        success_url = self.get_success_url(new_user)
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
        return super().get(request, *args, **kwargs)


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
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'
    next_page = '/blog/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return super().get(request, *args, **kwargs)


class PasswordResetView(views.PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = 'accounts/password_reset.html'
    success_url = '/blog/accounts/password_reset/done/'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class LogoutView(views.LogoutView):
    next_page = '/blog/'


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        return self.request.user.article_set.all()


class PasswordChangeView(LoginRequiredMixin, views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = '/blog/accounts/password_change/'
    form_class = forms.PasswordChangeForm

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        messages.info(self.request, 'Your password was successfully changed.')
        return super().form_valid(form)


class EmailChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/email_change.html'
    form_class = forms.EmailForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'new_email': request.user.email})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['new_email']
            request.user.save()
            messages.info(self.request, 'Your email was successfully changed.')
        return render(request, self.template_name, {'form': form})


class CreateArticleView(LoginRequiredMixin, TemplateView):
    template_name = 'create_article.html'
    form_class = forms.ArticleForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            tags = form.cleaned_data['tags']
            article = request.user.article_set.create(
                title=form.cleaned_data['title'],
                preview=form.cleaned_data['preview'],
                content=form.cleaned_data['content'],
                hidden=form.cleaned_data['hidden'],
                category=form.cleaned_data['category'],
            )
            for tag in tags:
                article.tags.add(tag)
            messages.info(self.request, 'Article created')
        return redirect(reverse('create_article'))


class ArticleEditView(LoginRequiredMixin, TemplateView):
    template_name = 'edit_article.html'
    form_class = forms.ArticleForm

    def get(self, request, *args, **kwargs):
        article = request.user.article_set.get(pk=kwargs['id'])
        form = self.form_class(initial={
            'tags': ', '.join(article.tags.names()),
            'title': article.title,
            'preview': article.preview,
            'content': article.content,
            'hidden': article.hidden,
            'category': article.category.id,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            tags = form.cleaned_data['tags']
            article = request.user.article_set.get(pk=kwargs['id'])
            article.title = form.cleaned_data['title']
            article.preview = form.cleaned_data['preview']
            article.content = form.cleaned_data['content']
            article.hidden = form.cleaned_data['hidden']
            article.category = form.cleaned_data['category']
            article.tags.clear()
            for tag in tags:
                article.tags.add(tag)
            article.save()
            messages.info(self.request, 'Changes was saved successfully')
            return redirect(reverse('edit_article', kwargs={'id': article.id}))
        return render(request, self.template_name, {'form': form})


class UserArticleList(LoginRequiredMixin, ListView):
    template_name = 'accounts/article_list.html'
    context_object_name = 'article_list'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def get_queryset(self, request):
        return Article.objects.filter(author=request.user).all()


class ArticleShowView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        article = request.user.article_set.get(pk=kwargs['id'])
        article.hidden = False
        article.save()
        return redirect(reverse('profile'))


class ArticleDeleteView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        article = request.user.article_set.get(pk=kwargs['id'])
        article_title = article.title
        article.delete()
        messages.info(self.request, f'Article \'{article_title}\' was deleted')
        return redirect(reverse('profile'))


class ArticleHideView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        article = request.user.article_set.get(pk=kwargs['id'])
        article.hidden = True
        article.save()
        return redirect(reverse('profile'))


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['id'])
        return render(request, self.template_name, {'article': article})


class AvatarView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/avatar_form.html'
    form_class = forms.AvatarForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if hasattr(request.user, 'profile'):
                old_image_path = request.user.profile.avatar.path
                request.user.profile.avatar = request.FILES['avatar']
                request.user.profile.save()
                os.remove(old_image_path)
            else:
                profile = Profile(avatar=request.FILES['avatar'], user=request.user)
                profile.save()
            messages.info(self.request, 'Your avatar was successfully changed.')
            return redirect(reverse('avatar'))
        return render(request, self.template_name, {'form': form})


class CommentsView(TemplateView):
    template_name = 'article.html'

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(article=kwargs['id']).order_by('submit_date')
        return JsonResponse(serializers.serialize('json', comments, use_natural_foreign_keys=True), safe=False)

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['id'])
        comment = article.comment_set.create(
            comment=request.POST.get('comment'),
            username=request.user.username,
            user=request.user,
            profile=request.user.profile
        )
        comment = Comment.objects.filter(id=comment.id)
        return JsonResponse(serializers.serialize('json', comment, use_natural_foreign_keys=True), safe=False)


class SearchView(ListView):
    template_name = 'search.html'
    context_object_name = 'article_list'
    paginate_by = 10

    def get_queryset(self):
        search_string = self.request.GET.get('q')
        tag = self.request.GET.get('tag')
        articles = Article.objects.filter(hidden=False)

        if tag is not None:
            articles = Article.objects.filter(tags__name__in=[tag])
        if search_string is not None:
            articles = articles.annotate(
                search=SearchVector('title', 'content', 'preview'),
            ).filter(search=search_string)

        return articles.order_by('-pub_date')
