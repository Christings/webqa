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
app_name = 'mleval'
urlpatterns = [
    # nvidia monitor
    # re_path(r'^gpu/$', views.gpu),
    re_path(r'^fanyi/detail/$', views.gpu_detail),
    # re_path(r'^gpu/del_task/$', views.gpu_del_task),
    # re_path(r'^gpu/del_host/$', views.gpu_del_host),
    # re_path(r'^gpu/task_start/$', views.gpu_task_start),
    # re_path(r'^gpu/task_stop/$', views.gpu_task_stop),
    # re_path(r'^gpu/task_edit/$', views.gpu_task_edit),
]