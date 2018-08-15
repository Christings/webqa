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
import html.parser
import urllib.request
import urllib.parse
import re
import html
import requests
import json
from threading import Thread
import time
from fanyi import requestData
# from pyonsg.fanyi import requestData

class ggThread(Thread):
	def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
		Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
		self._return = None

	def run(self):
		if self._target is not None:
			self._return = self._target(*self._args, **self._kwargs)

	def join(self):
		Thread.join(self)
		return self._return

def getResult_gg(fromlan,tolan,query):
	fy_begin = time.time()
	if fromlan == 'zh-CHS':
		fromlan_gg = 'zh-CN'
		if tolan in requestData.gg_language_dict:
			tolan_gg = requestData.gg_language_dict[tolan]
		else:
			tolan_gg = 'notsupport'
	else:
		if fromlan in requestData.gg_language_dict:
			fromlan_gg = requestData.gg_language_dict[fromlan]
		else:
			fromlan_gg = 'auto'
		tolan_gg = 'zh-CN'
	gg_result = ""
	if tolan_gg == 'notsupport':
		ret_result= 'dst not support'
	else:
		gg_req_list = query.split('\r\n')
		temlength = 1
		for gg_req in gg_req_list:
			if gg_req.strip()=='':
				continue
			else:
				try:
					agent = {
						'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
						'Host': 'www.googleapis.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
						'Upgrade-Insecure-Requests': '1',
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
						'X-Client-Data': 'CI22yQEIorbJAQjEtskBCKmdygEIqKPKARismMoB', 'Accept-Encoding': 'gzip, deflate, br',
						'Accept-Language': 'zh-CN,zh;q=0.9'}
					myurl = "https://www.googleapis.com/language/translate/v2?key=AIzaSyAXbOYLde61UfNKXqVADyXOFkmWvamjJQc&source=%s&target=%s&q=%s" % (fromlan_gg, tolan_gg, urllib.parse.quote(gg_req))
					url = 'http://wget.task.gd.ted/wget.php?url=' + urllib.parse.quote(myurl)
					resp = requests.get(url, headers=agent)
					try:
						resp = requests.get(myurl)
					except Exception as e:
						pass
					ggres = json.loads(resp.text)
					if len(gg_req_list) == temlength:
						gg_result += ggres['data']['translations'][0]['translatedText']
					else:
						gg_result += (ggres['data']['translations'][0]['translatedText'] + "|||")

					temlength += 1
				except Exception as e:
					gg_result = 'request error' + str(e)
		ret_result=gg_result
	fy_end = time.time()
	fy_cost = fy_end - fy_begin
	print('gg_cost', fy_cost)
	return ret_result

if __name__ == '__main__':

	result = getResult_gg('我爱你','zh','ko')
	#result = ggfy.TranslateByGoogle('我爱你','zh','ko')
	b=result['data']['translations'][0]['translatedText'].encode('utf-8')
	print(b.decode('utf-8'))
	#print(result['data']['translations'][0]['translatedText'])
