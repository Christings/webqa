# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, HttpResponse
from rbac.models import UserInfo
from rbac.service.init_permission import init_permission
from webqa import settings
import urllib,M2Crypto,json,base64,time
# import urllib,json,base64,time


def debug(request):
    return HttpResponse('let go')


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
    try:
        alive = request.session[settings.SESSION_MENU_KEY]
    except:
        alive = '0'
    if alive == '0':
        return redirect('login')
    else:
        return render(request, 'welcome.html')


def logout(request):
    response = redirect('https://login.sogou-inc.com/?appid=1220&sso_redirect=http://webqa.web.sjs.ted/login&targetUrl=')
    if ('uid' in request.COOKIES):
        response.delete_cookie("uid")
    return response
