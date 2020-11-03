import time

from django.urls import path
from . import views, models
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

app_name = 'dl'


@scheduler.scheduled_job('cron', day_of_week='0', hour='0', minute='01', second='01')
def clear_vote_num():
    models.Vote.objects.all().update(num=0, force_num=0)
    print('定时清空投票数,------------{}'.format(datetime.now()))


@scheduler.scheduled_job('cron', day_of_week='6', hour='23', minute='50', second='01')
def get_final_vote_name():
    models.Vote.objects.all().update(status=0)
    print('初始化投票状态---------------------{}'.format(datetime.now()))
    vote_info = models.Vote.objects.filter().values('vote_name', 'num', 'force_num', 'status')
    vote_num_list = []
    vote_force_list = []
    time.sleep(5)
    for e in vote_info:
        vote_num_list.append(e['num'])
        if e['force_num'] == 1:
            vote_force_list.append(e['force_num'])
            c = e['vote_name']
            models.Vote.objects.filter(vote_name=c).update(status=1)
            print('本周存在强制投票,{}开会---------------{}'.format(e['vote_name'], datetime.now()))
            break
    if len(vote_force_list) < 1:
        num = max(vote_num_list)
        a = models.Vote.objects.filter(num=num).values('vote_name')
        l = []
        for i in a:
            l.append(i['vote_name'])
        models.Vote.objects.filter(vote_name=l[0]).update(status=1)

    print('定时统计投票数,获取投票结果------------{}'.format(datetime.now()))


@scheduler.scheduled_job('cron', day_of_week='6', hour='23', minute='55', second='01')
def add_meeting_detail():
    vote_info = models.Vote.objects.all().values('vote_name', 'num', 'force_num')
    vote_data = []
    for i in vote_info:
        vote_data.append(str(list(i.values())))
    meet_name = models.Vote.objects.get(status=1).vote_name
    meet_date = models.Vote.objects.get(pk=meet_name.id).update_time.strftime('%W')
    models.Meeting.objects.create(meet_name=meet_name, meeting_date=meet_date, vote_list=vote_data)


scheduler.start()

urlpatterns = [
    path('', views.index, name='index'),
    path('login_action/', views.login_action, name='login_action'),
    path('register/', views.register, name='register'),
    path('vote/', views.vote_page, name='vote_page'),
    path('vote_action/', views.vote_action, name='vote_action'),
    path('logout/', views.logout, name='logout'),
    path('register_page/', views.register_page, name='register_page'),
]
