#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/5/17'
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
import requests
import urllib
import random
import time
import hmac
import hashlib
import base64
import json
from threading import Thread
import time
from fanyi import requestData
# from pyonsg.fanyi import requestData

class qqThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def getResult_qq(fromlan,tolan,query):
    # fy_begin=time.time()
    if fromlan == 'zh-CHS':
        fromlan_qq = 'zh'
        if tolan in requestData.qq_language_dict:
            tolan_qq = requestData.qq_language_dict[tolan]
        else:
            tolan_qq = 'notsupport'
    else:
        if fromlan in requestData.qq_language_dict:
            fromlan_qq = requestData.qq_language_dict[fromlan]
        else:
            fromlan_qq = 'auto'
        tolan_qq = 'zh'
    qq_result = ""
    if tolan_qq == 'notsupport':
        ret_result= 'dst not support'
    else:
        qq_req_list = query.split('\r\n')
        temlength = 1
        for qq_req in qq_req_list:
            if qq_req.strip()=='':
                continue
            else:
                try:
                    sec_id = "AKIDSuCMMC3cLyQgkfSgkMLHB1oCbw9Iqpz9"
                    sec_key = 'IWbVGqFUYZZZVHsHWecXN4a5WqzxmQuD'
                    salt = random.randint(10000, 99999)
                    Timestamp = int(time.time())
                    req_dict = {
                        'Action': 'TextTranslate',
                        'Nonce': salt,
                        'ProjectId': 0,
                        'Region': 'ap-beijing',
                        'SecretId': sec_id,
                        'Source': fromlan_qq,
                        'SourceText': qq_req,
                        'Target': tolan_qq,
                        'Timestamp': Timestamp,
                        'Version': '2018-03-21'
                    }
                    req_dict['Signature'] = buildSign(sec_key,**req_dict)
                    urlstr = ""
                    for key in req_dict:
                        urlstr += (key + '=' + urllib.parse.quote(str(req_dict[key])) + '&')
                    urlstr = urlstr[0:-1]
                    sufix = 'https://tmt.tencentcloudapi.com/?'
                    try:
                        resp = requests.get(sufix + urlstr)
                    except Exception as e:
                        pass
                    qqres = json.loads(resp.text)
                    if len(qq_req_list) == temlength:
                        qq_result += qqres['Response']['TargetText']
                    else:
                        qq_result += (qqres['Response']['TargetText'] + "|||")
                    temlength += 1
                except Exception as e:
                    print(e)
                    qq_result = 'request error ' + str(e)
        ret_result=qq_result
    # fy_end = time.time()
    # fy_cost = fy_end - fy_begin
    # print('qq_cost', fy_cost)
    return ret_result

def buildSign(sec_key,**req_dict):
    reqstr=''
    req_key_list=sorted(req_dict.keys())
    for key in req_key_list:
        reqstr+=(key+'='+str(req_dict[key])+'&')
    reqstr=(reqstr[0:-1])
    srcstr='GETtmt.tencentcloudapi.com/?'+reqstr
    h = hmac.new(bytes(sec_key,'utf-8'), bytes(srcstr,'utf-8'), hashlib.sha1).digest()
    signStr = base64.b64encode(h)
    return signStr.decode('utf-8')


if __name__ == '__main__':
    ret=dict()
    t_qq = qqThread(getResult_qq, ('zh', 'en', '我爱你'), getResult_qq.__name__)
    t_qq.start()
    t_qq.join()
    ret['qq_result'] = t_qq.get_result()
    print(ret['qq_result'])
