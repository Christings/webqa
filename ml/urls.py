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


app_name = 'ml'

router = routers.DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'rule', views.RuleViewSet)
router.register(r'field', views.FieldViewSet)

urlpatterns = [

    # crawler
    # re_path(r'^project', views.crawler_list),
    re_path(r'^project/add', views.crawler_add),
    re_path(r'^project/edit/(?P<id>\d+)$', views.crawler_edit),
    re_path(r'^project/run/(?P<id>\d+)$', views.crawler_run),
    re_path(r'^project_status/(?P<id>\d+)$', views.crawler_detail),

    # re_path(r'^project', include(router.urls)),
    re_path(r'^', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
