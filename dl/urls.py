from django.urls import path
from django.conf.urls import url
from . import views, models
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('cron', day_of_week='6', hour='23', minute='59', second='59')
def clear_vote_num():
    models.Vote.objects.all().update(num=0)
    print('定时清空投票数,------------{}'.format(datetime.now()))


@scheduler.scheduled_job('cron', day='1', hour='0', minute='0', second='1')
def clear_force_vote_num():
    models.Vote.objects.all().update(force_num=0)
    print('定时清空强制投票数,------------{}'.format(datetime.now()))


scheduler.start()

urlpatterns = [
    url(r'^login_action/', views.login_action),
    url(r'^register/', views.register),
    url(r'^vote/', views.vote_page),
    url(r'^login/', views.login),
    url(r'^vote_action/', views.vote_action),
    url(r'^logout/', views.logout),
    url(r'^register_page/', views.register_page),
]
