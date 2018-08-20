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

app_name = 'webqo'
urlpatterns = [
    # webqo
    re_path(r'^debug/$', views.debug),
    re_path(r'^debug_del$', views.debug_del),
    re_path(r'^debug_save$', views.debug_save),
    re_path(r'^debug_diff$', views.debug_diff),
    # re_path(r'^auto/$', views.auto),
    # re_path(r'^qo_automation(?P<page_id>\d*)$',views.qo_automation),
    # re_path(r'^qo_automation_add',views.qo_automation_add),
    # re_path(r'^qo_task_detail_(?P<task_id>\d+).html$',views.qo_task_detail),
    # re_path(r'^qo_task_readd$',views.qo_task_readd),
    # re_path(r'^qo_task_cancel',views.qo_task_cancel),

    # re_path(r'^qo_req$',views.qo_req),
    # re_path(r'^logout$',views.logout),
]
