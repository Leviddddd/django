"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from dl .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$', login),
    path(r'dl/', include('dl.urls')),
    path(r'admin/', admin.site.urls),
    url('login_action/', login_action),
    url(r'register/', register),
    url(r'vote/', vote_page),
    url(r'register_page/', register_page),
    url('login/', login),
    url('vote_action/', vote_action),
]
