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
    re_path(r'^automation(?P<page_id>\d*)$',views.automation),
    re_path(r'^automation_add',views.automation_add),
    re_path(r'^automation_detail_(?P<task_id>\d+).html$',views.automation_detail),
    re_path(r'^automation_restart$',views.automation_restart),
    re_path(r'^automation_cancel',views.automation_cancel),

    # re_path(r'^logout$',views.logout),
]
