from django.urls import path
from . import views
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def tick():
    print('Tick! The time is: %s' % datetime.now())


scheduler = BackgroundScheduler()
scheduler.add_job(tick, 'interval', seconds=30)
scheduler.start()

urlpatterns = [
    path('', views.login, name='login'),
    path('', views.login_action, name='login_action'),
    path('', views.register, name='register'),
    path('', views.register_page, name='register_page'),
]
