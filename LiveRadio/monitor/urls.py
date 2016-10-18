# -*- coding: utf-8 -*-
"""Monitor URL Configuration

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
from views import monitor, host, flow, flow_count, flow_detail, all_node, flow_count_history, export, auto_count,\
    p_manage, url_monitor, process_test
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^$', monitor, name='monitor'),
    url(r'^host/$', host, name='host'),
    url(r'^flow/$', flow, name='flow'),
    url(r'^flow/count$', flow_count, name='flow_count'),
    url(r'^flow/history$', flow_count_history, name='flow_count_history'),
    url(r'^flow/detail', flow_detail, name='flow_detail'),
    url(r'^all/$', all_node, name='all_node'),
    url(r'^export/$', export, name='export'),
    url(r'^auto_count/$', auto_count, name='auto_count'),
    url(r'^p_manage/$', p_manage, name='p_manage'),
    url(r'^process_test/$', process_test, name='process_test'),
    url(r'^url_monitor/$', url_monitor, name='url_monitor'),

]