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

app_name = 'wiki'
urlpatterns = [
    # wiki
    # re_path(r'^edit/$', views.edit),
    # re_path(r'^list/$', views.list),
    re_path(r'^wiki(?P<page_id>\d*)/$', views.wiki),
    re_path(r'^adds', views.add_wiki),
    re_path(r'^del$', views.del_wiki),
    re_path(r'^wiki_detail_(?P<task_id>\d+)$', views.wiki_detail),
    re_path(r'^edit$', views.edit_wiki),

]
