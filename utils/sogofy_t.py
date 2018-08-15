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

class sgThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def getResult_sg(inputHost,fromlan,tolan,reqtext,reqtype):
    ret = {'status': True, 'errro': None, 'data': None}
    try:
        if reqtype == 'xml':
            xmldata = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://api.microsofttranslator.com/V2"><soapenv:Header/><soapenv:Body><v2:Translate><v2:appId></v2:appId><v2:debug>true</v2:debug><v2:text>{_reqtext}</v2:text><v2:from>{_fromlan}</v2:from><v2:to>{_tolan}</v2:to><v2:contentType>text/plain</v2:contentType><v2:category>general</v2:category></v2:Translate></soapenv:Body></soapenv:Envelope>'''.format(
                _reqtext=reqtext, _fromlan=fromlan, _tolan=tolan)
            resp = requests.post(inputHost + '/' + reqtype, data=xmldata.encode('utf-8'))
            result = requestData.parseXmlRes(resp.text)
            ret['data'] = result['transRes']
            ret['debugInfo'] = result['DebugInfo'].replace('<br>', '')
            ret['requestStr'] = xmldata
        elif reqtype == 'alltrans_json':
            prefixq = '''{"to_lang": "''' + tolan + '''"''' + ''',"from_lang": "''' + fromlan + '''''''"''' + ''',"uuid": "74ad13f3-891c-45f6-99ef-f6de63173a20","sendback": "title"''' + ''',"trans_frag": ['''
            suffix = ""
            alljquery = ""
            temp_len = 1
            reqlst = reqtext.split('\r\n')
            for req in reqlst:
                if temp_len == len(reqlst):
                    suffix += '''{"sendback": "title","id":"''' + str(
                        temp_len) + '''","text":"''' + req + '''''''"}]}'''
                else:
                    suffix += '''{"sendback": "title","id":"''' + str(
                        temp_len) + '''","text":"''' + req + '''''''"},'''
                temp_len += 1
                alljquery = prefixq + suffix
            resp = requests.post(inputHost + '/' + reqtype, data=alljquery.encode('utf-8'))
            ret['data'] = requestData.parseAlljRes(resp.text)
            ret['debugInfo'] = resp.text
            ret['requestStr'] = alljquery
        else:
            ret['error'] = "Error:未知的请求类型"
            ret['status'] = False
    except Exception as e:
        ret['status'] = False
        ret['error'] = 'request error ' + str(e)
        pass
    return ret



if __name__ == '__main__':
    # ret=dict()
    # ret = getResult_sg('http://ywhub01.fy.sjs.ted:12000', 'zh-CHS', 'en', '我爱你', 'xml')
    t_sg = sgThread(getResult_sg, ('http://ywhub01.fy.sjs.ted:12000','zh-CN', 'en', '我爱你','xml'), getResult_sg.__name__)
    t_sg.start()
    t_sg.join()
    ret = t_sg.get_result()
    print(ret['data'])
