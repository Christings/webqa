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
from django.urls import re_path,include
from . import views

app_name = 'publicEnv'


urlpatterns = [
    # svcheck
    re_path(r'^p99/$', views.pnine),
    re_path(r'^p99/del_line/$', views.del_line),
    re_path(r'^p99/detail/$', views.pnine_detail),
    # deadlink
    re_path(r'^deadlink/$', views.deadlink),
    re_path(r'^deadlink/resolved/$', views.resolved),
    re_path(r'^deadlink/get_urllist/$', views.get_urllist),
    # svcheck
    re_path(r'^svcheck/$', views.svcheck),
    re_path(r'^svcheck/detail/$', views.svcheck_detail),
]
