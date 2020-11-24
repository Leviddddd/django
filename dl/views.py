import json
import time

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dl import models
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime
from django.utils.datetime_safe import datetime

data = {'status': 3, 'error': '参数错误'}
success = {'status': 1, 'error': '成功'}
failure = {'status': 2, 'error': '失败'}


def index(request):
    return render(request, 'login.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            user_obj = models.AuthUser.objects.get(username=username)
            request.session['user'] = user_obj.id
            return HttpResponseRedirect('/dl/vote/')
        else:
            return render(request, 'login.html', {'error': '请输入正确的账号或密码!'})
    else:
        return render(request, 'login.html', {'error': '请求错误'})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/dl/')
    return response


@login_required(login_url='/dl/')
def vote_page(request):
    user_id = request.session.get('user', '')
    vote_info = models.Vote.objects.all().values('id', 'vote_name', 'num', 'force_num')
    vote_msg = []
    vote_name = models.Vote.objects.filter(status=1).values('status', 'vote_name')
    if len(vote_name):
        final_vote_name = vote_name[0]['vote_name']
    else:
        final_vote_name = '未有投票结果'
    for e in vote_info:
        e['user_id'] = user_id
        vote_msg.append(e)
    return render(request, 'index.html', {'vote_info': vote_msg, 'vote_name': final_vote_name})


def register_page(request):
    return render(request, 'tset.html')


def register(request):
    HttpResponseRedirect('/dl/register_page/')
    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        local_user = models.AuthUser.objects.all().values('username')
        print(local_user)
        local_user_list = []
        for i in local_user:
            local_user_list.append(i['username'])
        if username in local_user_list:
            return render(request, 'tset.html', {'error': '账号已存在，注册失败'})
        else:
            user = User.objects.create_user(username=username, password=password)
            if user:
                return HttpResponseRedirect('/dl/')
            else:
                return render(request, '/dl/register_page/', {'error': '注册账号失败'})
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


@login_required
def vote_action(request):
    try:
        userId = int(request.POST.get('user_id', ''))
        voteId = int(request.POST.get('vote_id', ''))
        voteType = int(request.POST.get('vote_type', ''))
        user_vote_record = models.UserVote.objects.filter(user_id=userId, vote_type=voteType).values()
        force_vote = models.Vote.objects.all().values('vote_name', 'force_num')
        force_vote_name_list = []
        for name in force_vote:
            if name['force_num'] >= 1:
                force_vote_name_list.append(name['vote_name'])
        if len(force_vote_name_list):
            is_force_vote = {'status': 1, 'error': '本周{}已强制开会，无法投票'.format(force_vote_name_list[0])}
            return JsonResponse(is_force_vote)
        else:
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
                    if now_week > old_week and now_year == old_year or now_year > old_year:
                        user_vote_info = models.UserVote.objects.get(user_id=userId, vote_type=voteType)
                        user_vote_info.vote_id = voteId
                        user_vote_info.save()

                        vote_info = models.Vote.objects.get(id=voteId)
                        vote_info.num += 1
                        vote_info.save()
                        return JsonResponse(success)
                    else:
                        failure['error'] = '当前不可投票'
                        return JsonResponse(failure)
                # 强制投票
                elif voteType == 2:
                    if month > old_month and now_year == old_year or now_year > old_year:
                        force_num = models.Vote.objects.get(id=voteId)
                        force_num.force_num += 1
                        force_num.save()
                        user_force_vote_info = models.UserVote.objects.get(user_id=userId, vote_type=voteType)
                        user_force_vote_info.vote_id = voteId
                        user_force_vote_info.save()
                        return JsonResponse(success)
                    else:
                        return JsonResponse(failure)
                else:
                    return JsonResponse(failure)
            else:
                obj = models.UserVote(user_id=userId, vote_id=voteId, vote_type=voteType)
                obj.save()
                if voteType == 1:
                    vote_info = models.Vote.objects.get(id=voteId)
                    vote_info.num += 1
                    vote_info.save()
                    return JsonResponse(success)
                elif voteType == 2:
                    vote_info = models.Vote.objects.get(id=voteId)
                    vote_info.force_num += 1
                    vote_info.save()
                    return JsonResponse(success)
    except Exception as e:
        return HttpResponse(e)



