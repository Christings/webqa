#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/3/28'
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
from xml.etree import ElementTree
import json
import random
language_dict = {
                        'en' : '英',
                        'fr' : '法',
                        'ru' : '俄',
                        'ko' : '韩',
                        'ja' : '日',
                        'ar' : '阿拉伯语',
                        'et' : '爱沙尼亚语',
                        'bg' : '保加利亚语',
                        'pl' : '波兰语',
                        'bs-Latn' : '波斯尼亚语',
                        'fa' : '波斯语',
                        'mww' : '白苗文',
                        'da' : '丹麦语',
                        'de' : '德语',
                        'fi' : '芬兰语',
                        'tlh-Qaak' : '克林贡语(piqaD)',
                        'tlh' : '克林贡语',
                        'hr' : '克罗地亚语',
                        'otq' : '克雷塔罗奥托米语',
                        'ca' : '加泰隆语',
                        'cs' : '捷克语',
                        'ro' : '罗马尼亚语',
                        'lv' : '拉脱维亚语',
                        'ht' : '海地克里奥尔语',
                        'lt' : '立陶宛语',
                        'nl' : '荷兰语',
                        'ms' : '马来语',
                        'mt' : '马耳他语',
                        'pt' : '葡萄牙语',
                        'sl' : '斯洛文尼亚语',
                        'th' : '泰语',
                        'tr' : '土耳其语',
                        'sr-Latn' : '塞尔维亚语(拉丁文)',
                        'sr-Cyrl' : '塞尔维亚语(西里尔文)',
                        'sk' : '斯洛伐克语',
                        'sw' : '斯瓦希里语',
                        'af' : '南非荷兰语',
                        'no' : '挪威语',
                        'es' : '西班牙语',
                        'uk' : '乌克兰语',
                        'ur' : '乌尔都语',
                        'el' : '希腊语',
                        'hu' : '匈牙利语',
                        'cy' : '威尔士语',
                        'yua' : '尤卡坦玛雅语',
                        'he' : '希伯来语',
                        'it' : '意大利语',
                        'hi' : '印地语',
                        'id' : '印度尼西亚语',
                        'vi' : '越南语',
                        'sv' : '瑞典语',
                        'yue' : '粤语(繁体)',
                        'fj' : '斐济语',
                        'FIL' : '菲律宾语',
                        'sm' : '萨摩亚语',
                        'to' : '汤加语',
                        'ty' : '塔希提语',
                        'mg' : '马尔加什语',
                        'bn' : '孟加拉语',
}


bd_language_dict = {
                        'auto' : '自动检测',
                        'zh' : '中文',
                        'en' : 'en',
                        'yue' : 'yue',
#                        'wyw' : '文言文',
                        'ja' : 'jp',
                        'ko' : 'kor',
                        'fr' : 'fra',
                        'es': 'spa',
                        'th' : 'th',
                        'ar' : 'ara',
                        'ru' : 'ru',
                        'pt' : 'pt',
                        'de' : 'de',
                        'it' : 'it',
                        'el' : 'el',
                        'nl' : 'nl',
                        'pl' : 'pl',
                        'bg' : 'bul',
                        'et' : 'est',
                        'da' : 'dan',
                        'fi' : 'fin',
                        'cs' : 'cs',
                        'ro' : 'rom',
                        'sl' : 'slo',
                        'sv' : 'swe',
                        'hu' : 'hu',
#                        'cht':'繁体中文',
                        'vi' : 'vie',
}

gg_language_dict = {
                        'en':'en',
                        'fr':'fr',
                        'ru':'ru',
                        'ko':'ko',
                        'ja':'ja',
                        'ar':'ar',
                        'de':'de',
                        'pt':'pt',
                        'es':'es',
                        'hu':'hu',
                        'it':'it',
                        'pl':'pl',
                        'cs':'cs',
                        'nl':'nl',
                        'da':'da',
                        'fi':'fi',
                        'tr':'tr',
                        'sv':'sv',
}


yd_language_dict = {
                        'en':'en',
                        'fr':'fr',
                        'ru':'ru',
                        'ko':'ko',
                        'ja':'ja',
                        'es':'es',
                        'pt':'pt',
}

qq_language_dict = {
                        'en':'en',
                        'ja':'jp',
                        'ko':'kr',
                        'de':'de',
                        'fr':'fr',
                        'es':'es',
                        'it':'it',
                        'tr':'tr',
                        'ru':'ru',
                        'pt':'pt',
                        'vi':'vi',
                        'id':'id',
                        'ms':'ms',
                        'th':'th',
                        'auto':'自动检测',
}

def parseJsonRes(xml_str):
    resparse = json.loads(xml_str)
    result = resparse['translate_result']['docs']
    result_dict=dict()
    resultstr=""
    temlen=1
    for sub_res in result:
        result_dict[sub_res['id']] = sub_res['title'] + '|||' + sub_res['abstract']
    for i in range(1,len(result_dict)+1):
        if temlen == len(result_dict):
            resultstr += result_dict[str(i)]
        else:
            resultstr += (result_dict[str(i)] + "^^^")
        temlen += 1
    return resultstr

def parseJsonReq(xml_str):
    try:
        resparse = json.loads(xml_str)
        chinese_query = resparse['translate_struct']['chinese_query']
        english_query = resparse['translate_struct']['english_query']
        result = resparse['translate_struct']['docs']
        result_dict=dict()
        result_dict['docs']=list()
        for sub_res in result:
            result=dict()
            result[sub_res['id']] = sub_res['title'] + '|||' + sub_res['abstract']
            result_dict['docs'].append(result)
        result_dict['chinese_query'] = chinese_query
        result_dict['english_query'] = english_query
        result_dict['status'] = True
    except Exception as e:
        result_dict=dict()
        result_dict['status'] = False
    return result_dict

def JsonResult(json_str):
    try:
        resparse = json.loads(json_str)
        result = resparse['translate_result']['docs']
        result_dict=dict()
        result_dict['docs']=list()
        for sub_res in result:
            tempNum = random.randint(1,3)
            result=dict()
            result[sub_res['id']] = sub_res['title'] + '|||' + sub_res['abstract']
            result_dict['docs'].append(result)
        result_dict['status'] = True
        result_dict['chinese_query'] = resparse['translate_result']['chinese_query']
    except Exception as e:
        result_dict=dict()
        result_dict['status'] = False
        
    return result_dict


def allJsonResult(json_str):
    try:
        resparse = json.loads(json_str[8:-1])
        result = resparse['trans_result']
        result_dict = dict()
        result_dict['docs'] = list()
        for sub_res in result:
            tempNum = random.randint(1, 3)
            result = dict()
            result[sub_res['id']] = sub_res['trans_text']
            result_dict['docs'].append(result)
        result_dict['status'] = True
        result_dict['red_mark'] = resparse['red_mark']
        result_dict['trans_red_query'] = resparse['trans_red_query']
        result_dict['en_red_query'] = resparse['en_red_query']
        result_dict['ch_red_query'] = resparse['ch_red_query']
    except Exception as e:
        result_dict = dict()
        result_dict['status'] = False
    return result_dict

def parseAlljRequest(xml_str):
    try:
        resparse = json.loads(xml_str)
        from_lang = resparse['from_lang']
        to_lang = resparse['to_lang']
        result = resparse['trans_frag']
        result_dict=dict()
        result_dict['docs']=list()
        for sub_res in result:
            result=dict()
            result[sub_res['id']] = sub_res['sendback'] + '|||' + sub_res['text']
            result_dict['docs'].append(result)
        result_dict['from_lang'] = from_lang
        result_dict['to_lang'] = to_lang
        result_dict['status'] = True
    except Exception as e:
        result_dict=dict()
        result_dict['status'] = False
    return result_dict


def parseAlljRes(xml_str):
    resparse = json.loads(xml_str)
    result = resparse['trans_result']
    result_dict=dict()
    resultstr=""
    temlen=1
    for sub_res in result:
        result_dict[sub_res['id']]=sub_res['trans_text']
    for i in range(1,len(result_dict)+1):
        if temlen == len(result_dict):
            resultstr += result_dict[str(i)]
        else:
            resultstr += (result_dict[str(i)] + "|||")
        temlen += 1
    return resultstr


def parseXmlRes(xml_str):
    result_dic=dict()
    ns={'parent':'http://schemas.xmlsoap.org/soap/envelope/','child':'http://fanyi.sogou.com/'}
    try:
        root=ElementTree.fromstring(xml_str)
    except Exception as e:
        print(e)
        result_dic['wrongres']='wrongres:'+str(e)
        return result_dic
    for node in root.findall('parent:Body',ns):
        for body in node.findall('child:TranslateResponse',ns):
            if body.find('child:TranslateResult',ns) is not None:
                result_dic['transRes']=body.find('child:TranslateResult',ns).text
            else:
                result_dic['transRes']=''
            if body.find('child:DebugInfo',ns) is not None:
                result_dic['DebugInfo']=body.find('child:DebugInfo',ns).text
            else:
                result_dic['DebugInfo']=''
    return result_dic

def getUniNum(string):
        try:
                string=string.strip()
                query=""
                for uchar in string:
                        query+="&#"+str(ord(uchar))+";"
                return query
        except Exception as e:
                pass
