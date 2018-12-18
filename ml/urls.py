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
from rest_framework import routers

app_name = 'publicEnv'

router = routers.DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'rule', views.RuleViewSet)
router.register(r'field', views.FieldViewSet)

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
    # crawler
    # re_path(r'^project', views.crawler_list),
    re_path(r'^project/add', views.crawler_add),
    re_path(r'^project/(?P<id>\d+)$', views.crawler_detail),

    # re_path(r'^project', include(router.urls)),
    re_path(r'^', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
