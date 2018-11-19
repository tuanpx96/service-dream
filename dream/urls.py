"""dream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from dream_users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/email/', user_views.LoginEmailAPI.as_view()),
    path('reset-password/', user_views.ResetPassword.as_view()),
    path('login/facebook/', user_views.LoginFacebookAPI.as_view()),
    path('register/', user_views.RegisterEmailAPI.as_view()),
    path('confirm/<token>/', user_views.ConfirmEmailAPI.as_view()),
    path('logout/', user_views.LogoutAPI.as_view()),
]
