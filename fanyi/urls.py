#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/8/6'
# ----------Dragon be here!----------
              ┏━┓      ┏━┓
            ┏━┛ ┻━━━━━━┛ ┻━━┓
            ┃       ━       ┃
            ┃  ━┳━┛   ┗━┳━  ┃
            ┃       ┻       ┃
            ┗━━━┓      ┏━━━━┛
                ┃      ┃神兽保佑
                ┃      ┃永无BUG！
                ┃      ┗━━━━━━━━━┓
                ┃                ┣━┓
                ┃                ┏━┛
                ┗━━┓ ┓ ┏━━━┳━┓ ┏━┛
                   ┃ ┫ ┫   ┃ ┫ ┫
                   ┗━┻━┛   ┗━┻━┛
"""
from django.urls import re_path
from . import views
app_name = 'fanyi'
urlpatterns = [
    # debug
    re_path(r'^debug/$', views.debug),
    # bbk
    re_path(r'^bbk/$', views.bbk),
    # debug and bbk share
    re_path(r'^del_line/$', views.del_line),
    re_path(r'^req_info_save/$', views.req_info_save),
    # nvidia monitor
    re_path(r'^gpu/$', views.gpu),
    re_path(r'^gpu_detail/$', views.gpu_detail),
    re_path(r'^gpu_del_task/$', views.gpu_del_task),
    re_path(r'^gpu_del_host/$', views.gpu_del_host),
    re_path(r'^gpu_task_start/$', views.gpu_task_start),
    re_path(r'^gpu_task_stop/$', views.gpu_task_stop),


]