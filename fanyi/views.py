# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, HttpResponse
from rbac.models import UserInfo
from rbac.service.init_permission import init_permission
from django.conf import settings
import urllib,M2Crypto,json,base64,time



def login(request):
    login_url = "https://login.sogou-inc.com/?appid=1220&sso_redirect=http://webqa.web.sjs.ted/login&targetUrl="
    ptoken = ""
    try:
        ptoken = request.GET['ptoken']
    except Exception as e:
        print(e)
        print('00000','0000000000001')
        pass
    response = None
    if ('uid' not in request.COOKIES and ptoken is ""):
        print(11111111111)
        return redirect(login_url)
    if (ptoken != "" ):#login request callback
        print(2222222222222,ptoken)
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
            if userStatus.exists()==False:
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
        print(33333333333333333333)
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

    # return render(request, 'index.html')
    return render(request, 'father.html')


def test(request):
    # 前端请求过来，首页显示多级菜单
    # 请求过来，拿到session中的信息，拿到菜单，权限数据 -- 定制数据结构 -- 作显示
    menu = request.session[settings.SESSION_MENU_KEY]
    all_menu = menu[settings.ALL_MENU_KEY]
    permission_url = menu[settings.PERMISSION_MENU_KEY]

    print(all_menu)
    print('-----------')
    print(permission_url)

    all_menu = [
        {'id': 1, 'title': '订单管理', 'parent_id': None}, {'id': 2, 'title': '库存管理', 'parent_id': None},
        {'id': 3, 'title': '生产管理', 'parent_id': None}, {'id': 4, 'title': '生产调查', 'parent_id': None}
    ]

    # 定制数据结构
    all_menu_dict = {}
    for item in all_menu:
        item['status'] = False
        item['open'] = False
        item['children'] = []
        all_menu_dict[item['id']] = item

    all_menu_dict = {
        1: {'id': 1, 'title': '订单管理', 'parent_id': None, 'status': False, 'open': False, 'children': []},
        2: {'id': 2, 'title': '库存管理', 'parent_id': None, 'status': False, 'open': False, 'children': []},
        3: {'id': 3, 'title': '生产管理', 'parent_id': None, 'status': False, 'open': False, 'children': []},
        4: {'id': 4, 'title': '生产调查', 'parent_id': None, 'status': False, 'open': False, 'children': []}
    }

    permission_url = [
        {'title': '查看订单', 'url': '/order', 'menu_id': 1},
        {'title': '查看库存清单', 'url': '/stock/detail', 'menu_id': 2},
        {'title': '查看生产订单', 'url': '/produce/detail', 'menu_id': 3},
        {'title': '产出管理', 'url': '/survey/produce', 'menu_id': 4},
        {'title': '工时管理', 'url': '/survey/labor', 'menu_id': 4},
        {'title': '入库', 'url': '/stock/in', 'menu_id': 2},
        {'title': '排单', 'url': '/produce/new', 'menu_id': 3}
    ]

    request_rul =  '/stock/in'
    import re

    for url in permission_url:
        # 添加两个状态：显示 和 展开
        url['status'] = True
        pattern = url['url']
        if re.match(pattern, request_rul):
            url['open'] = True
        else:
            url['open'] = False

        # 将url添加到菜单下
        all_menu_dict[url['menu_id']]["children"].append(url)

        # 显示菜单：url 的菜单及上层菜单 status: true
        pid = url['menu_id']
        while pid:
            all_menu_dict[pid]['status'] = True
            pid = all_menu_dict[pid]['parent_id']

        # 展开url上层菜单：url['open'] = True, 其菜单及其父菜单open = True
        if url['open']:
            ppid = url['menu_id']
            while ppid:
                all_menu_dict[ppid]['open'] = True
                ppid = all_menu_dict[ppid]['parent_id']

    # 整理菜单层级结构：没有parent_id 的为根菜单， 并将有parent_id 的菜单项加入其父项的chidren内
    final_menu = []
    for i in all_menu_dict:
        if all_menu_dict[i]['parent_id']:
            pid = all_menu_dict[i]['parent_id']
            parent_menu = all_menu_dict[pid]
            parent_menu['children'].append(all_menu_dict[i])
        else:
            final_menu.append(all_menu_dict[i])

    print('final_menu ---------------\n',final_menu)


    return HttpResponse('...')
