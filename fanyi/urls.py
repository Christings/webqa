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
    re_path(r'^debug_del_line/$', views.debug_del_line),
    re_path(r'^debug_info_save/$', views.debug_info_save),
    # re_path(r'^users/new/$', views.users_new),
    # re_path(r'^users/edit/(?P<id>\d+)/$', views.users_edit),
    # re_path(r'^users/delete/(?P<id>\d+)/$', views.users_delete),
]