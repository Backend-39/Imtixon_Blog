from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *


class MainView(View):
    def get(self, request):
        articles = Article.objects.filter(article_type='ommaviy')
        context = {
            'global_articles': articles
        }
        return render(request, 'index.html', context)
    

class GlobalArticlesInfoView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        context = {
            'article': article
        }
        return render(request, 'article_info.html', context)

class RegisterView(View):
    def get(self, request):
        form = UserForm()
        context = {
            'register_form': form
        }
        return render(request, 'register.html', context)
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-page')
        context = {
            "register_form": form
        }
        return render(request, 'register.html', context)

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'login_form': form
        }
        return render(request, 'login.html', context)
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('user-home')
        context = {
            'login_form': form,
            'auth_failed': "Foydalanuvchi nomi yoki parol noto'g'ri kiritildi!"
        }
        return render(request, 'login.html', context)
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')
    
class UserHomeView(LoginRequiredMixin, View):
    def get(self, request):
        articles = Article.objects.filter(article_type='ommaviy')
        context = {
            'global_articles': articles
        }
        return render(request, 'user_home.html', context)
    
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')
    
class UserGlobalArticleInfoView(LoginRequiredMixin, View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        context = {
            'article': article
        }
        return render(request, 'user_article_info.html', context)

class UserArticlesView(LoginRequiredMixin, View):
    def get(self, request):
        article_form = ArticleTagForm()
        articles = Article.objects.filter(user=request.user)
        context={
            'article_form': article_form,
            'articles': articles
        }
        return render(request, 'user_articles.html', context)
    def post(self, request):
        if request.POST.get('add_article'):
            form = ArticleTagForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                title = cleaned_data.get('title')
                context = cleaned_data.get('context')
                tags = cleaned_data.get('tags')
                article_type = cleaned_data.get('article_type')

                article = Article.objects.create(
                    title = title,
                    context = context,
                    user = request.user,
                    article_type = article_type
                )
                article.tags.set(tags)
        elif request.POST.get('add_tag'):
            name = request.POST.get('name')
            if name:
                Tag.objects.create(
                    name=name
                )
        return redirect('user-articles')
                

class DeleteUserArticleView(LoginRequiredMixin,View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        article.delete()
        return redirect('user-articles')

class EditUserArticleView(LoginRequiredMixin, View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        data = {
            'title': article.title,
            'context': article.context,
            'tags': article.tags.all(),
            'article_type': article.article_type
        }
        form = ArticleTagForm(data=data)
        context = {'article_form': form}
        return render(request, 'edit_article.html', context)
    def post(self, request, slug):
        form = ArticleTagForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            title = cleaned_data.get('title')
            context = cleaned_data.get('context')
            tags = cleaned_data.get('tags')
            article_type = cleaned_data.get('article_type')

            article = get_object_or_404(Article, slug=slug)

            article.title = title
            article.context = context
            article.article_type = article_type
            article.tags.set(tags)
            article.save()
        return redirect('user-articles')