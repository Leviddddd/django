import json
import time

from django.contrib import auth
from django.contrib.auth.models import User
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from dl import models
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime
from django.utils.datetime_safe import datetime
from dl.models import Vote

data = {'status': 3, 'error': '参数错误'}
success = {'status': 1, 'error': '成功'}
failure = {'status': 2, 'error': '失败'}


def login(request):
    return render(request, 'login.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            response = HttpResponseRedirect('/vote/')
            # request.session['user'] = username
            user_id = models.AuthUser.objects.filter(username=username).values('id')
            if len(user_id):
                user_id = models.AuthUser.objects.filter(username=username).values('id')[0]['id']
                request.session['user'] = user_id
                return response
            else:
                return render(request, 'login.html', {'error': '用户id为空，请重新登录'})
        else:
            return render(request, 'login.html', {'error': '请输入正确的账号或密码!'})
    else:
        return render(request, 'login.html', {'error': 'username or password error!!!'})


def vote_page(request):
    user_id = request.session.get('user', '')
    vote_info = models.Vote.objects.all().values('id', 'vote_name', 'num', 'force_num')
    vote_msg = []
    for e in vote_info:
        e['user_id'] = user_id
        vote_msg.append(e)
    return render(request, 'index.html', {'vote_info': vote_msg})


def register_page(request):
    return render(request, 'tset.html')


def register(request):
    HttpResponseRedirect('/register_page')
    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        local_user = models.AuthUser.objects.filter().values('username')
        user_list = []
        for i in local_user:
            user_list.append(i['username'])
        print(user_list)
        if username in user_list:
            return render(request, 'tset.html', {'error': '账号已存在，注册失败'})
        else:
            user = User.objects.create_user(username=username, password=password)
            if user:
                return HttpResponseRedirect('/login')
            else:
                return render(request, '/register_page', {'error': 'false'})
    except Exception as e:
        raise e


def get_time_info(info, time_stramp=None):
    if time_stramp:
        now_time = int(time_stramp)
    else:
        now_time = int(time.time())
    now_time_stramp = time.localtime(now_time)
    now_strftime = time.strftime("%Y%m%d", now_time_stramp)
    time_info = datetime.strptime(now_strftime, "%Y%m%d").strftime("%{}".format(info))
    return int(time_info)


@csrf_exempt
def vote_action(request):
    userId = int(request.POST.get('user_id'))
    voteId = int(request.POST.get('vote_id'))
    voteType = int(request.POST.get('vote_type'))
    try:
        user_vote_record = models.UserVote.objects.filter(vote_id=voteId, user_id=userId, vote_type=voteType).values()
        if user_vote_record:
            update_time = str(user_vote_record[0]['update_time']).split('+')[0]
            timeArray = time.strptime(update_time, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            now_year = get_time_info('Y')
            old_year = get_time_info('Y', timeStamp)
            old_week = get_time_info('W', timeStamp)
            now_week = get_time_info('W')
            old_month = get_time_info('m', timeStamp)
            month = int(time.localtime().tm_mon)
            # 周投票
            if voteType == 1:
                if now_week > old_week and now_year == old_year:
                    models.UserVote.objects.filter(id=user_vote_record[0]['id']).update(update_time=datetime.now())
                    vote_num = models.Vote.objects.filter(id=voteId).values('num')[0]['num']
                    models.Vote.objects.filter(id=voteId).update(num=vote_num + 1)
                    return JsonResponse(success)
                elif now_year > old_year:
                    models.UserVote.objects.filter(id=user_vote_record[0]['id']).update(update_time=datetime.now())
                    vote_num = models.Vote.objects.filter(id=voteId).values('num')[0]['num']
                    models.Vote.objects.filter(id=voteId).update(num=vote_num + 1)
                    return JsonResponse(success)
                else:
                    failure['error'] = '当前不可投票'
                    return JsonResponse(failure)
            # 强制投票
            elif voteType == 2:
                if month > old_month and now_year == old_year or now_year > old_year:
                    force_num = models.Vote.objects.filter(id=voteId).values('force_num')[0]['force_num']
                    models.Vote.objects.filter(id=voteId).update(force_num=force_num + 1)
                    models.UserVote.objects.filter(id=user_vote_record[0]['id']).update(update_time=datetime.now())
                    return JsonResponse(success)
                else:
                    return JsonResponse(failure)
            else:
                return JsonResponse(data)
        else:
            obj = models.UserVote(user_id=userId, vote_id=voteId, vote_type=voteType)
            obj.save()
            if voteType == 1:
                vote_num = models.Vote.objects.filter(id=voteId).values('num')[0]['num']
                models.Vote.objects.filter(id=voteId).update(num=vote_num + 1)
                return JsonResponse(success)
            elif voteType == 2:
                force_num = models.Vote.objects.filter(id=voteId).values('force_num')[0]['force_num']
                models.Vote.objects.filter(id=voteId).update(force_num=force_num + 1)
                return JsonResponse(success)

    except Exception as e:
        raise e
