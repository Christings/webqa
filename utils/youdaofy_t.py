#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/5/16'
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
import random
import hashlib
import urllib
import requests
import json
from threading import Thread
import time
from fanyi import requestData
# from pyonsg.fanyi import requestData

class ydThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def getResult_yd(fromlan,tolan,query):
    # fy_begin = time.time()
    if fromlan == 'zh-CHS':
        fromlan_yd = 'zh-CHS'
        if tolan in requestData.yd_language_dict:
            tolan_yd = requestData.yd_language_dict[tolan]
        else:
            tolan_yd = 'notsupport'
    else:
        if fromlan in requestData.yd_language_dict:
            fromlan_yd = requestData.yd_language_dict[fromlan]
        else:
            fromlan_yd = 'auto'
        tolan_yd = 'zh-CHS'
    yd_result = ""
    if tolan_yd == 'notsupport':
        ret_result= 'dst not support'
    else:
        yd_req_list = query.split('\r\n')
        temlength = 1
        for yd_req in yd_req_list:
            if yd_req.strip()=='':
                continue
            else:
                try:
                    appKey = "6ae9815f6d6129db"
                    sec_key = "3DfMT6NVupkamXtBu2z5BF4rVAMMA9YC"
                    salt = random.randint(10000, 99999)
                    signid = sign(appKey,salt,sec_key,yd_req)
                    myurl = 'http://openapi.youdao.com/api' + '?appKey=' + appKey + '&q=' + urllib.parse.quote(
                        yd_req) + '&from=' + fromlan_yd + '&to=' + tolan_yd + '&salt=' + str(salt) + '&sign=' + signid
                    try:
                        resp = requests.get(myurl)
                    except Exception as e:
                        pass

                    ydres = json.loads(resp.text)
                    if len(yd_req_list) == temlength:
                        yd_result += ydres['translation'][0]
                    else:
                        yd_result += (ydres['translation'][0] + "|||")
                    temlength += 1
                except Exception as e:
                    yd_result = 'request error' + str(e)
        ret_result=yd_result
    # fy_end = time.time()
    # fy_cost = fy_end - fy_begin
    # print('yd_cost', fy_cost)
    return ret_result


def sign(appKey,salt,sec_key,query):
    hl = hashlib.md5()
    sign_str = appKey + query + str(salt) + sec_key
    hl.update(sign_str.encode(encoding='utf-8'))
    x = hl.hexdigest()
    return x


# if __name__ == '__main__':
#     bdfy = Youdaofy()
#     result = bdfy.getResult('zh','en','我爱你')
#     print(result['translation'])
#     #print(result['trans_result'][0]['dst'])


