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
    re_path(r'^debug/del_line/$', views.del_line),
    re_path(r'^debug/req_info_save/$', views.req_info_save),
    # bbk
    re_path(r'^bbk/$', views.bbk),
    re_path(r'^bbk/del_line/$', views.del_line),
    re_path(r'^bbk/req_info_save/$', views.req_info_save),
    # nvidia monitor
    re_path(r'^gpu/$', views.gpu),
    re_path(r'^gpu/detail/$', views.gpu_detail),
    re_path(r'^gpu/del_task/$', views.gpu_del_task),
    re_path(r'^gpu/del_host/$', views.gpu_del_host),
    re_path(r'^gpu/task_start/$', views.gpu_task_start),
    re_path(r'^gpu/task_stop/$', views.gpu_task_stop),
    re_path(r'^gpu/task_edit/$', views.gpu_task_edit),
    # man eval
    re_path(r'^man_eval/$', views.man_eval),
    re_path(r'^man_eval/detail/$', views.man_eval_detail),
    re_path(r'^man_eval/cancel/$', views.man_eval_cancal),
    re_path(r'^man_eval/readd/$', views.man_eval_readd),
]