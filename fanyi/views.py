# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, HttpResponse
from rbac.models import UserInfo
from rbac.service.init_permission import init_permission
from utils import pagination
from fanyi import models
from fanyi import requestData
import urllib,M2Crypto,json,base64,time,requests
# import urllib,json,base64,time,requests

def auth(func):
    def inner(request,*args,**kwargs):
        login_url = "https://login.sogou-inc.com/?appid=1220&sso_redirect=http://webqa.web.sjs.ted/login&targetUrl="
        try:
            user_id = request.COOKIES.get('uid')
            if not user_id:
                return redirect(login_url)
        except:
            return redirect(login_url)
        return func(request,*args,**kwargs)
    return inner


def debug_del_line(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        models.ReqInfo.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))


@auth
def debug_info_save(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'errro': None, 'data': None}
    inputHost = request.POST.get('inputHost')
    lan_sel = request.POST.get('lan_sel')
    fromto = request.POST.get('inlineRadioOptions')
    reqtext = request.POST.get('reqtext')
    result = request.POST.get('result')
    if result is None:
        result=""
    reqtype = request.POST.get('reqtype')
    try:
        models.ReqInfo.objects.create(host_ip=inputHost, trans_direct=lan_sel, isfromzh=fromto, req_text=reqtext,result=result, user_fk_id=user_id,reqtype=reqtype)
        ret['inputHost']=inputHost
        ret['lan_sel']=lan_sel
        ret['fromto']=fromto
        ret['reqtext']=reqtext
        ret['result']=result
        ret['reqtype']=reqtype
    except Exception as e:
        ret['error'] = "Error:" + str(e)
        print(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

@auth
def debug(request):
    uid = request.COOKIES['uid']
    # uid = 'zhangjingjun'
    if request.method == 'GET':
        page = request.GET.get('page')
        current_page = 1
        if page:
            current_page = int(page)
        try:
            req_list = models.ReqInfo.objects.filter(user_fk_id=uid).order_by('id')[::-1]
            req_list = models.ReqInfo.objects.order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(req_list), 15, 5)
            data = req_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/fanyi/debug?page=")
        except Exception as e:
            print(e)
            pass
        return render(request, 'fanyi/fy_debug.html',{'user_id': uid,'li': data,'page_str': page_str})
    elif request.method == 'POST':
        ret = {'status': True, 'errro': None, 'data': None}
        inputHost = request.POST.get('inputHost')
        reqtype = request.POST.get('reqtype')
        lan_sel = request.POST.get('lan_sel')
        fromto = request.POST.get('inlineRadioOptions')
        reqtext = request.POST.get('reqtext')
        query = requestData.getUniNum(reqtext)
        if fromto == 'tozh':
            fromlan = lan_sel
            tolan = 'zh-CHS'
        else:
            fromlan = 'zh-CHS'
            tolan = lan_sel
        output = 'host={_host}, reqtype={_reqtype},from_lang={_fromlan},to_lang={_tolan},query={_query}'.format(
            _host=inputHost, _reqtype=reqtype, _fromlan=fromlan, _tolan=tolan, _query=reqtext)
        try:
            if reqtype == 'xml':
                xmldata = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://api.microsofttranslator.com/V2"><soapenv:Header/><soapenv:Body><v2:Translate><v2:appId></v2:appId><v2:debug>true</v2:debug><v2:text>{_reqtext}</v2:text><v2:from>{_fromlan}</v2:from><v2:to>{_tolan}</v2:to><v2:contentType>text/plain</v2:contentType><v2:category>general</v2:category></v2:Translate></soapenv:Body></soapenv:Envelope>'''.format(
                    _reqtext=reqtext, _fromlan=fromlan, _tolan=tolan)
                resp = requests.post(inputHost + '/' + reqtype, data=xmldata.encode('utf-8'))
                result = requestData.parseXmlRes(resp.text)
                ret['transResult'] = result['transRes']
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
                ret['transResult'] = requestData.parseAlljRes(resp.text)
                ret['debugInfo'] = resp.text
                ret['requestStr'] = alljquery
            else:
                ret['error'] = "Error:未知的请求类型"
                ret['status'] = False
            ret['fromlan'] = fromlan
            ret['tolan'] = tolan
            ret['lan_sel'] = lan_sel
            ret['host'] = inputHost
            ret['reqtype'] = reqtype
        except Exception as e:
            print(e)
            ret['error'] = "Error:" + str(e)
            ret['status'] = False
        return HttpResponse(json.dumps(ret))


def login(request):
    login_url = "https://login.sogou-inc.com/?appid=1220&sso_redirect=http://webqa.web.sjs.ted/login&targetUrl="
    ptoken = ""
    try:
        ptoken = request.GET['ptoken']
    except Exception as e:
        print(e)
        pass
    response = None
    if ('uid' not in request.COOKIES and ptoken is ""):
        return redirect(login_url)
    if (ptoken != "" ):#login request callback
        message = urllib.parse.unquote(ptoken)
        strcode = base64.b64decode(message)
        pkey = M2Crypto.RSA.load_pub_key('/search/odin/pypro/webqa/public.pem')
        output = pkey.public_decrypt(strcode, M2Crypto.RSA.pkcs1_padding)
        try:
            json_data = json.loads(output.decode('utf-8'))
            uid = json_data['uid']
            login_time = int(json_data['ts'])/1000 #s
            print(uid)
            userStatus = UserInfo.objects.filter(username=uid)
            if userStatus.exists() == False:
                insertInfo = UserInfo(username=uid)
                insertInfo.save()
        except Exception as e :
            print(e)
            uid = ""
            login_time = 0
        now_time = time.time()
        if (uid != "" and now_time - login_time < 60):
            user_obj = UserInfo.objects.filter(username=uid).first()
            init_permission(request, user_obj)
            response = redirect('/index/')
            if ('uid' not in request.COOKIES):
                response.set_cookie("uid", uid)
        else:
            response = None
    elif ('uid' in request.COOKIES):#already login
        try:
            uid = request.COOKIES['uid']
        except:
            uid = ""
        if (uid != ""):
            user_obj = UserInfo.objects.filter(username=uid).first()
            init_permission(request, user_obj)
            response = redirect('/index/')
            if ('uid' not in request.COOKIES):
                response.set_cookie("uid", uid)
        else:
            response = None
    if (response is None):
        return redirect(login_url)
    return response


def index(request):
    return render(request, 'welcome.html')


def logout(request):
    response = redirect('https://login.sogou-inc.com/?appid=1220&sso_redirect=http://webqa.web.sjs.ted/login&targetUrl=')
    if ('uid' in request.COOKIES):
        response.delete_cookie("uid")
    return response
