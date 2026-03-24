"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main-page'),
    path('global-articles/<slug:slug>/', GlobalArticlesInfoView.as_view(), name='global-articles-info'),

    path('user/auth/register/', RegisterView.as_view(), name='register-page'),
    path('user/auth/login/', LoginView.as_view(), name='login-page'),
    path('user/auth/logout/', LogoutView.as_view(), name='logout'),

    path('user/home/global-articles/', UserHomeView.as_view(), name='user-home'),
    path('user/profile/', ProfileView.as_view(), name='user-profile'),
    path('user/home/articles/<slug:slug>/', UserGlobalArticleInfoView.as_view(), name='user-articles-info'),
    path('user/home/articles/', UserArticlesView.as_view(), name='user-articles'),
    path('user/home/articles/<slug:slug>/delete', DeleteUserArticleView.as_view(), name='delete-user-article'),
    path('user/home/articles/<slug:slug>/edit/', EditUserArticleView.as_view(), name='edit-article')
]
