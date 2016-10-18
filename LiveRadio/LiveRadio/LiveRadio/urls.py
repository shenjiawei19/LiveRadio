# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    #下载文件路由配置
    url(r"uploads/(?P<path>.*)$",
        "django.views.static.serve",
        {"document_root":settings.MEDIA_ROOT,}),
    url(r'^admin/', admin.site.urls),
    url(r'^',include('radio.urls')),
    url(r'monitor/',include('monitor.urls'))
]