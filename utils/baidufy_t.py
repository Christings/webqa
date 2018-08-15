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

class bdThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def getResult_bd(fromlan,tolan,query):
    # fy_begin = time.time()
    if fromlan == 'zh-CHS':
        fromlan_bd = 'zh'
        if tolan in requestData.bd_language_dict:
            tolan_bd = requestData.bd_language_dict[tolan]
        else:
            tolan_bd = 'notsupport'
    else:
        if fromlan in requestData.bd_language_dict:
            fromlan_bd = requestData.bd_language_dict[fromlan]
        else:
            fromlan_bd = 'auto'
        tolan_bd = 'zh'
    bd_result = ""
    if tolan_bd == 'notsupport':
        ret_result= 'dst not support'
    else:
        bd_req_list = query.split('\r\n')
        temlength = 1
        for bd_req in bd_req_list:
            if bd_req.strip()=='':
                continue
            else:
                try:
                    appid = "20180516000160525"
                    sec_key = "4QoUOqERE4Mx_dD2S_MQ"
                    salt = random.randint(10000, 99999)
                    hl = hashlib.md5()
                    sign_str = appid + bd_req + str(salt) + sec_key
                    hl.update(sign_str.encode(encoding='utf-8'))
                    signid = hl.hexdigest()
                    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate' + '?appid=' + appid + '&q=' + urllib.parse.quote(
                        bd_req) + '&from=' + fromlan_bd + '&to=' + tolan_bd + '&salt=' + str(salt) + '&sign=' + signid
                    try:
                        resp = requests.get(myurl)
                    except Exception as e:
                        pass
                    bdres = json.loads(resp.text)
                    if len(bd_req_list) == temlength:
                        bd_result += bdres['trans_result'][0]['dst']
                    else:
                        bd_result += (bdres['trans_result'][0]['dst'] + "|||")
                    temlength += 1
                except Exception as e:
                    bd_result = 'request error' + str(e)
        ret_result = bd_result
    # fy_end=time.time()
    # fy_cost = fy_end-fy_begin
    # print('bd_cost',fy_cost)
    return ret_result

def sign(self,query):
    hl = hashlib.md5()
    sign_str = self.appid + query + str(self.salt) + self.sec_key
    hl.update(sign_str.encode(encoding='utf-8'))
    x = hl.hexdigest()
    return x



if __name__ == '__main__':
    #bdfy = Badufy()
    #result = bdfy.getResult('zh','ara','我想你')
    #result = getResult_bd('zh-CHS', 'ar', '我想你')
    #print(result)
    #print(result['trans_result'][0]['dst'])
    t = bdThread(getResult_bd,('zh-CHS', 'ar', '我想你'),getResult_bd.__name__)
    t.start()
    t.join()
    print(t.get_result())


