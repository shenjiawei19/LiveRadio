# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render, redirect, HttpResponse,render_to_response,HttpResponseRedirect,RequestContext
# from django.core.urlresolvers import reverse
# from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
# from django.views.decorators.csrf import csrf_exempt
# from django.db import connection
# from django.db.models import Count,Q
# import hashlib
from models import *
from forms import *
from datetime import datetime
from func.func import not_null_none, permission_base
import json
import time
from func.pag import pag
# import pdb
logger = logging.getLogger('radio.views')
# pdb.set_trace()
# Create your views here.
# from django.views.decorators.cache import cache_page
# 导致报错'dict' object has no attribute 'streaming'


# 登入首页
def do_login(request):
    username = request.COOKIES.get('username','')
    if username is not '':
        group = User.objects.get(username=username).group
        user_manage, live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
        return render(request, 'index.html', locals())
    else:
        pass
    login_form = LoginForm()
    return render(request, 'login.html', locals())
    # return render_to_response("index.html",  {"dicts":dicts,},context_instance = RequestContext(request))


# 主页
def index(request):
    app = request.POST.get('app', None)
    if app == 'Monitor':
        response = HttpResponseRedirect('/monitor/')

        username = request.POST.get('username', 'xxx')

        response.set_cookie('username', username, 3600)


        username = request.COOKIES.get('username', '')

        request.session['username'] = username
        return HttpResponseRedirect('/monitor/')

    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'index.html', locals())
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)

                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    # print request.session.
                    login(request,user)
                else:
                    reason = "用户名密码错误"
                    return render(request, 'login.html',locals())
                # task = Task.objects.all().order_by('-start_time')
                response = HttpResponseRedirect('/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username', username, 3600)
                username = request.COOKIES.get('username','')
                return response
                # return render(request, 'index.html', locals())
            else:
                reason = "用户名密码错误"
                return render(request, 'login.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:

        logger.error(e)
    login_form = LoginForm()
    reason = "用户名密码错误"
    return render(request, 'login.html', locals())


# 登出
def do_logout(request):
    try:
        response = HttpResponseRedirect('/index/')
        #清理cookie里保存username
        response.delete_cookie('username')
        logout(request)
    except Exception as e:
        print e
        logger.error(e)
    return response


# 用户管理
def user_manage(request):
    try:
        username = request.COOKIES.get('username','')
        if username is not '':
            user = User.objects.filter(Q(is_delete=0)).order_by('level')
            add = AddUserForm()
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'user_list.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 添加用户
def add_user(request):
    if request.method == 'POST':
        add_u = AddUserForm(request.POST)
        admin_name = request.COOKIES.get('username','')
        if add_u.is_valid():
            # 登录
            email = username = add_u.cleaned_data["email"]
            password = add_u.cleaned_data["password"]
            re_password = add_u.cleaned_data["re_password"]
            group = Group.objects.get(name=request.POST.get('group'))

            if password == re_password:
                try:
                    if User.objects.get(email=email):
                        reason = {"error": "用户已存在"}
                        return HttpResponseRedirect('/user/')
                except Exception as e:
                    try:
                        User.objects.create_user(username=username,email=email,password=password,group=group,level=group.id)
                        admin_log = Op_log(op_name=admin_name, op_detail='添加 '+username+' 用户')
                        admin_log.save()
                        return HttpResponseRedirect('/user/')
                    except Exception as e:
                        print e
        else:
            reason = "用户名密码错误"
            return HttpResponseRedirect('/user/')
    return HttpResponseRedirect('/user/')


# 删除用户
def del_user(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            if request.method == 'GET':
                delname = request.GET.get('delname', 'xxx')
                u = User.objects.get(username=delname)
                u.is_delete=1
                u.save()
                admin_log = Op_log(op_name=username, op_detail='删除 '+delname+' 用户')
                admin_log.save()
        return HttpResponseRedirect('/user/')
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


# 修改密码页面
def chg_pwd(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            pwd_form = PwdForm()
        return render(request, 'chg_pwd.html', locals())
    except Exception as e:
        logger.error(e)
        login_form = LoginForm()
    return render(request, 'login.html', locals())


# 完成修改密码页面
def finish_pwd(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            pwd_form = PwdForm(request.POST)
            if pwd_form.is_valid():
                user = User.objects.get(username=username)
                old_pwd = pwd_form.cleaned_data["old_pwd"]
                new_pwd = pwd_form.cleaned_data["new_pwd"]
                re_new_pwd = pwd_form.cleaned_data["re_new_pwd"]
                if user.check_password(old_pwd) is True and (new_pwd == re_new_pwd):
                    user.password = make_password(new_pwd)
                    user.save()
                else:
                    pwd_form = PwdForm()
                    return render(request, 'chg_pwd.html', locals())
        return render(request, 'index.html', locals())
    except Exception as e:
        logger.error(e)
        login_form = LoginForm()
    return render(request, 'login.html', locals())


# 直播频道管理
def live_channel(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            channel_all = Channel.objects.all()
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            channel_form = AddChannelForm()
            return render(request, 'live_channel.html', locals())
    except Exception as e:
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())

# 开关
def open_channel(request,id=''):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            if id is not '':
                open = request.GET.get('open', '')
                if open is not '':
                    c = Channel.objects.get(pk=id)
                    if c.is_open == 0:
                        c.is_open = 1
                        c.open_memo = '开'
                    else:
                        c.is_open = 0
                        c.open_memo = '关'
                    c.save()
            channel_all = Channel.objects.all()
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            channel_form = AddChannelForm()

            return render(request, 'live_channel.html', locals())
    except Exception as e:
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())



# 增加直播频道
def add_channel(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            channel = AddChannelForm(request.GET)
            if channel.is_valid():
                channel_id = channel.cleaned_data["channel"]
                signal = channel.cleaned_data["signal"]
                info = channel.cleaned_data["channel_info"]
                url = channel.cleaned_data["url"]
                channel_add = Channel(channel=channel_id, signal=signal, channel_info=info,url=url)
                channel_add.save()
                admin_log = Op_log(op_name=username, op_detail=u'添加 ' + channel_id + '' + u' 直播频道')
                admin_log.save()
                return HttpResponseRedirect('/live_channel/')
            else:

                return render(request, 'live_channel.html', locals())
    except Exception as e:
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 编辑直播频道信息
def edit_channel(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            if request.method == 'GET':
                channel = request.GET.get('channel', None)
                signal = request.GET.get('signal', None)
                info = request.GET.get('info', None)
                url = request.GET.get('url', None)
                chl = Channel.objects.get(channel=channel)
                chl.channel = channel
                chl.signal = signal
                chl.channel_info = info
                chl.url = url
                chl.save()
                admin_log = Op_log(op_name=username, op_detail='修改了 '+channel+' 频道信息')
                admin_log.save()
        return HttpResponseRedirect('/live_channel/')
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 删除直播频道
def del_channel(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            if request.method == 'GET':
                del_channel = request.GET.get('delchannel', None)
                print del_channel[4:]
                u = Channel.objects.get(channel=del_channel[4:])
                print u.signal
                u.delete()
                admin_log = Op_log(op_name=username, op_detail='删除 '+del_channel+' 直播频道')
                admin_log.save()
        return HttpResponseRedirect('/live_channel/')
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 直播频道接口：给出指定时间，返回开始时间和关闭是都大于的所有直播任务，返回json
# 127.0.0.1:8000/channel_api?u=shiyun&p=e18375ee830ace536fdc4fcc9b1d6a78
def channel_api(request):
    try:
        if request.GET.get('u', None) == 'shiyun' and (request.GET.get('p', None) =='e18375ee830ace536fdc4fcc9b1d6a78'):
            result = {}
            channel_all = Channel.objects.all()
            result['data'] = {}
            for c in channel_all:
                result['data'][c.id] = {'channel':c.channel,'signal': c.signal, 'info': c.channel_info,'url':c.url}
            result['status'] = 'ok'
        else:
            result = {
                'status': 0
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as e:
        print e
        result = {
                'status': 0
        }
        logger.error(e)
    return HttpResponse(json.dumps(result), content_type="application/json")

# 频道接口：返回任务状态，返回json
# 127.0.0.1:8000/channel_open?u=shiyun&p=e18375ee830ace536fdc4fcc9b1d6a78
def channel_open(request):
    try:
        if request.GET.get('u', None) == 'shiyun' and (request.GET.get('p', None) =='e18375ee830ace536fdc4fcc9b1d6a78'):
            result = {}
            channel_all = Channel.objects.all()
            result['data'] = {}
            for c in channel_all:
                result['data'][c.id] = {'channel':c.channel,'signal': c.signal, 'info': c.channel_info,'url':c.url,'is_open':c.is_open}
            result['status'] = 'ok'
        else:
            result = {
                'status': 0
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as e:
        print e
        result = {
                'status': 0
        }
        logger.error(e)
    return HttpResponse(json.dumps(result), content_type="application/json")

# 直播任务管理
def live_radio(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            radio = AddRadioForm()
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            radio_task = Task.objects.filter(is_delete=0, finish_time__gte=now).order_by('start_time')
            count,radio_task = pag(request,radio_task,20)
            future = "active"
            history = ""
            custom = ""
            hidden = "hidden"
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'content.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())




# 查看历史直播任务
def view_history_radio(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            radio = AddRadioForm()
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            radio_task = Task.objects.filter(is_delete=0, finish_time__lt=now).order_by('start_time')
            d,radio_task = pag(request,radio_task,20)
            future = ""
            history = "active"
            custom = ""
            hidden = "hidden"
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'content.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 高级检索
def custom_radio(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            radio = AddRadioForm()
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            id = request.GET.get('search_id', "")
            title = request.GET.get('search_title', "")
            description = request.GET.get('search_description', "")
            task_status = request.GET.get('search_status', "")
            channel_number = request.GET.get('search_channel', "")
            start_time = request.GET.get('search_start_time_range1', "")
            start_time_2 = request.GET.get('search_start_time_range2', "")
            finish_time = request.GET.get('search_finish_time_range1', "")
            finish_time_2 = request.GET.get('search_finish_time_range2', "")
            list_search = not_null_none(id=id, title=title, description=description, task_status=task_status,
                          channel=channel_number, start_time=start_time, start_time_2=start_time_2,
                          finish_time=finish_time, finish_time_2=finish_time_2,is_delete=0)
            future = ""
            history = ""
            custom = "active"
            radio_task = Task.objects.filter(**list_search)
            d,radio_task = pag(request,radio_task,20)
            if len(list_search) > 1:
                hidden = "hidden"
            else:
                hidden = ""
                radio_task = ""
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'content.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 添加直播任务
def add_radio(request):
    local_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            radio = AddRadioForm(request.GET)
            if radio.is_valid():
                print "ok"
                title = radio.cleaned_data["title"]
                description = radio.cleaned_data["description"]
                channel = radio.cleaned_data["channel"]
                start_time = radio.cleaned_data["start_time"]
                finish_time = radio.cleaned_data["finish_time"]
                s_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
                l_time = datetime.strptime(local_time, "%Y-%m-%d %H:%M")
                if (finish_time > start_time) and (start_time > local_time) and \
                        (((s_time - l_time).seconds > 3600) or ((s_time - l_time).days >= 1)):
                    try:
                        task = Task(title=title, description=description, channel=channel,
                                    start_time=start_time, finish_time=finish_time)
                        task.save()
                        admin_log = Op_log(op_name=username, op_detail=u'添加 '+title+''+channel+u' 直播任务')
                        admin_log.save()
                        return HttpResponseRedirect('/live_radio/')
                    except Exception as e:
                        print e
                        logger.error(e)
                        reason = {"error": "请保证结束时间大约开始时间，开始时间大于当前时间，标题唯一"}
                        return HttpResponse(json.dumps(reason), content_type="application/json")
                else:
                    reason = {"error": "请保证结束时间大约开始时间，开始时间大于当前时间，标题唯一"}
                    return HttpResponse(json.dumps(reason), content_type="application/json")
            else:
                reason = {"error": "格式错误"}
                return HttpResponse(json.dumps(reason), content_type="application/json")
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 删除直播任务
def del_radio(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            if request.method == 'GET':
                del_radio = request.GET.get('delradioid', None)
                u = Task.objects.get(pk=int(del_radio[4:]))
                u.is_delete = 1
                u.save()
                admin_log = Op_log(op_name=username, op_detail='删除 '+del_radio+' 直播任务')
                admin_log.save()
        return HttpResponseRedirect('/live_radio/')
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 修改直播任务
def edit_radio(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            if request.method == 'GET':
                radio_id = request.GET.get('radio_id', None)
                radio_title = request.GET.get('radio_title', None)
                radio_description = request.GET.get('radio_description', None)
                radio_channel = request.GET.get('radio_channel', None)
                radio_start_time = request.GET.get('radio_start_time', None)
                radio_finish_time = request.GET.get('radio_finish_time', None)
                radio = Task.objects.get(pk=radio_id)
                radio.title = radio_title
                radio.description = radio_description
                radio.channel = radio_channel
                radio.start_time = radio_start_time
                radio.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                radio.finish_time = radio_finish_time
                radio.save()
                admin_log = Op_log(op_name=username, op_detail='修改了 '+radio_title+' '+radio_channel+' 直播任务')
                admin_log.save()
        return HttpResponseRedirect('/live_radio/')
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 直播任务接口：给出指定时间，返回结束大于大于给定时间的所有直播任务，返回json
# 127.0.0.1:8000/live_api?u=shiyun&p=e18375ee830ace536fdc4fcc9b1d6a78&t=2016-08-0811:11:11

def live_api(request):
    try:
        if request.GET.get('u', None) == 'shiyun' and (request.GET.get('p', None) =='e18375ee830ace536fdc4fcc9b1d6a78'):
            t = request.GET.get('t', None)
            t = t[:10]+' '+t[11:]
            reason = {}
            if t:
                # radio = Task.objects.filter(start_time__gte=t, finish_time__gte=t, is_delete=0)
                radio = Task.objects.filter(finish_time__gte=t, is_delete=0)
                for r in radio:
                    reason[r.id] = {'channel':r.channel,'start_time': str(r.start_time)[:19], 'finish_time': str(r.finish_time)[0:19]}
        else:
            reason = {
                'status': 0
            }
            return HttpResponse(json.dumps(reason), content_type="application/json")
    except Exception as e:
        print e
        reason = {
                'status': 0
        }
        logger.error(e)
    return HttpResponse(json.dumps(reason), content_type="application/json")


# 节点管理
def node(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            # 通过主表查子表
            Node.objects.filter(node_detail__node_status=2).update(node_status=2)
            node_all = Node.objects.style_node()
            if not Node.objects.filter(node_detail__node_status=4):
                Node.objects.filter(~Q(node_status = 0)).update(node_status=0)
            count,node_all = pag(request,node_all,20)
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'node.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 节点详情
def node_detail(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            ip = request.GET.get('name', None)
            detail = Node_detail.objects.style_node_detail(ip)
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'node_detail.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 操作记录查询
def op_log(request):
    try:
        username = request.COOKIES.get('username', '')
        if username is not '':
            log = Op_log.objects.all().order_by('-id')
            group = User.objects.get(username=username).group
            user_manage,live_channel, live_manage, node_manage, op_manage = permission_base(str(group))
            return render(request, 'operation_log.html', locals())
    except Exception as e:
        print e
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 测试页面
def test(request):
    return render(request, 'test.html', locals())