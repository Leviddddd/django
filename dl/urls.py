from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('', views.login_action, name='login_action'),
    path('', views.register, name='register'),
    path('', views.register_page, name='register_page'),
]
