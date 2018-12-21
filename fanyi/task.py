#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/12/14'
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
from __future__ import absolute_import

from celery import shared_task,task
from celery import Celery
from webqa import celery_app
import os,traceback,time


@celery_app.task
def get_fanyi_result(task_id):
    try:
        task_status = os.system('/root/anaconda3/bin/python3 /search/odin/pypro/webqa/utils/getdiff_byxml.py %d &' % task_id)
    except Exception as e:
        traceback.print_exc()
        pass
    return task_status


@celery_app.task
def get_gpu_detail(runningid,req_id):
    try:
        task_status = os.system('python3 /search/odin/pypro/webqa/utils/monitor.py %s %s &' % (str(runningid), req_id))
        # task_status = os.system('python3 /Users/zhangjingjun/work/code/webqa/utils/monitor.py %s %s &' % (str(runningid), req_id))
    except Exception as e:
        traceback.print_exc()
        pass
    return task_status
