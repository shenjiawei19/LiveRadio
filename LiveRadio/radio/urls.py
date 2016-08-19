# -*- coding: utf-8 -*-
"""Myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from views import do_login, index, do_logout, user_manage, live_radio, node, add_user, \
    del_user, add_radio, del_radio, edit_radio, view_history_radio, custom_radio, op_log, \
    node_detail, test, live_api, chg_pwd, finish_pwd
from django.views.decorators.cache import cache_page
urlpatterns = [
    url(r'^$', do_login, name='do_login'),
    url(r'^index/$', index, name='index'),
    url(r'^logout/$', do_logout, name='do_logout'),
    url(r'^user/$', user_manage, name='user_manage'),
    url(r'live_radio/$', live_radio, name='live_radio'),
    url(r'node/$', node, name='node'),
    url(r'node_detail/', node_detail, name='node_detail'),
    url(r'^user/add_user/$', add_user, name='add_user'),
    url(r'^user/del_user/$', del_user, name='del_user'),
    url(r'^live_radio/add_radio/$', add_radio, name='add_radio'),
    url(r'^live_api/$', live_api, name='live_api'),
    url(r'^test/$', test,name='test'),
    url(r'^live_radio/del_radio/$', del_radio, name='del_radio'),
    url(r'^live_radio/edit_radio/$', edit_radio, name='edit_radio'),
    url(r'^live_radio/view_history_radio/$', view_history_radio, name='view_history_radio'),
    url(r'^live_radio/custom_radio/$', custom_radio, name='custom_radio'),
    url(r'^op_log/$', op_log, name='op_log'),
    url(r'^chg_pwd/$', chg_pwd, name='chg_pwd'),
    url(r'^finish_pwd/$', finish_pwd, name='finish_pwd')

]