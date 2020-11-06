import time

from django.db.models import Max, Min, Avg
from django.urls import path, re_path
from . import views, models
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

app_name = 'dl'


@scheduler.scheduled_job('cron', day_of_week='0', hour='0', minute='00', second='01')
def clear_vote_num():
    models.Vote.objects.all().update(num=0, force_num=0)
    print('定时清空投票数,------------{}'.format(datetime.now()))


@scheduler.scheduled_job('cron', day_of_week='6', hour='23', minute='50', second='01')
# @scheduler.scheduled_job('interval', seconds=5)
def get_final_vote_name():
    models.Vote.objects.all().update(status=0)
    print('初始化投票状态---------------------{}'.format(datetime.now()))
    vote_force_name = models.Vote.objects.filter(force_num=1).values('vote_name')[:1]
    if vote_force_name:
        vote_force_name = list(vote_force_name[0].keys())[0]
        models.Vote.objects.filter(vote_name=vote_force_name).update(status=1)
        print('本周存在强制投票,{}开会---------------{}'.format(vote_force_name, datetime.now()))
    else:
        num = list(models.Vote.objects.aggregate(Max('num')).values())[0]
        print(num)
        if num >= 1:
            vote_num_name = list(models.Vote.objects.filter(num=num).values('vote_name')[:1][0].values())[0]
            models.Vote.objects.filter(vote_name=vote_num_name).update(status=1)
            print('定时统计投票数,获取投票结果------------{}'.format(datetime.now()))

# @scheduler.scheduled_job('interval', seconds=5)
@scheduler.scheduled_job('cron', day_of_week='6', hour='23', minute='55', second='01')
def add_meeting_detail():
    vote_info = models.Vote.objects.filter(status=1).values()[:1]
    if vote_info:
        vote_info = vote_info[0]
        meet_name = vote_info['vote_name']
        meet_date = vote_info['update_time'].strftime('%W')
    else:
        meet_name = '未有投票结果'
        meet_date = datetime.now().strftime('%W')
    vote_data = models.Vote.objects.all().values('vote_name', 'num', 'force_num')
    vote_data_list = []
    for i in vote_data:
        vote_data_list.append(tuple(i.values()))
    models.Meeting.objects.create(meet_name=meet_name, meeting_date=meet_date, vote_list=vote_data_list)
    print('插入开会结果数据---------------------------{}'.format(datetime.now()))


scheduler.start()

urlpatterns = [
    path('', views.index, name='index'),
    path('login_action/', views.login_action, name='login_action'),
    path('register/', views.register, name='register'),
    path('account_login/', views.index),
    path('vote/', views.vote_page, name='vote_page'),
    path('vote_action/', views.vote_action, name='vote_action'),
    path('logout/', views.logout, name='logout'),
    path('register_page/', views.register_page, name='register_page'),
]
