# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, HttpResponse
from rbac.models import UserInfo
from django.forms.models import model_to_dict
from rbac.service.init_permission import init_permission
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from utils import pagination
from fanyi import models
from utils import baidufy_t
from utils import youdaofy_t
from utils import qqfy_t
from utils import sogofy_t
import M2Crypto
import urllib
import json
import base64
import time
import os
import signal

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


# man eval
@auth
@csrf_exempt
def man_eval_readd(request):
    # user_id = "zhangjingjun"
    user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'errro': None, 'data': None}
    re_add_task_d = request.POST.get('task_id')
    try:
        task_detail = models.ManEval.objects.get(id=re_add_task_d)
        task_detail_todic = model_to_dict(task_detail)
        task_detail_todic.pop('id')
        task_detail_todic['create_time'] = get_now_time()
        task_detail_todic['start_time'] = ""
        task_detail_todic['end_time'] = ""
        task_detail_todic['status'] = 0
        task_detail_todic['errorlog'] = ""
        task_detail_todic['finished'] = 0
        task_detail_todic['runningIP'] = ""
        task_detail_todic['user'] = user_id
        models.ManEval.objects.create(**task_detail_todic)
    except Exception as e:
        print(e)
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


def man_eval_cancal(request):
    ret = {'status': True, 'errro': None, 'data': None}
    try:
        cancel_id = request.POST.get('task_id')
        models.ManEval.objects.filter(id=cancel_id).update(status=6)
    except Exception as e:
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


@auth
def man_eval_detail(request):
    # user_id="zhangjingjun"
    user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('tasknum')
    page = request.GET.get('page')
    current_page = 1
    if page:
        current_page = int(page)
    task_detail = models.ManEval.objects.filter(id=task_id).first()
    task_diff_detail = models.ManEvalDiff.objects.filter(diff_task_id=task_id).order_by('id')[::-1]
    page_obj = pagination.Page(current_page, len(task_diff_detail), 4, 9)
    data = task_diff_detail[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("/man_eval/detail/?tasknum=" + task_id + '&page=')
    hubsvn = str_unix2br(task_detail.hubsvn)
    sersvn = str_unix2br(task_detail.sersvn)
    loginfo = str_unix2br(task_detail.errorlog)
    return render(request, 'fanyi/man_eval_detail.html',{'user_id': user_id,'task_detail': task_detail,'hubsvn':hubsvn,'sersvn': sersvn, 'loginfo':loginfo,'li': data, 'page_str': page_str})


@auth
def man_eval(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        page = request.GET.get('page')
        current_page = 1
        if page:
            current_page = int(page)
        try:
            task_list = models.ManEval.objects.order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(task_list), 16, 9)
            data = task_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/man_eval?page=")

        except Exception as e:
            print(e)
            pass
        return render(request, 'fanyi/man_eval.html',{'user_id': user_id, 'li': data,'page_str': page_str})
    elif request.method == 'POST':
        ret = {'status': True, 'errro': None, 'data': None}
        hubsvn = str_dos2unix(request.POST.get('hub_svn'))
        sersvn = str_dos2unix(request.POST.get('server_svn'))
        hubcfgip = str_dos2unix(request.POST.get('hub_conf_ip'))
        hubcfguser = str_dos2unix(request.POST.get('hub_conf_user'))
        hubcfgpassw = str_dos2unix(request.POST.get('hub_conf_pass'))
        hubcfgpath = str_dos2unix(request.POST.get('hub_conf_path'))
        hubdatapath = str_dos2unix(request.POST.get('hub_data_path'))
        sercfgip = str_dos2unix(request.POST.get('ser_conf_ip'))
        sercfguser = str_dos2unix(request.POST.get('ser_conf_user'))
        sercfgpassw = str_dos2unix(request.POST.get('ser_conf_pass'))
        sercfgpath = str_dos2unix(request.POST.get('ser_conf_path'))
        serdatapath = str_dos2unix(request.POST.get('ser_data_path'))
        queryip = str_dos2unix(request.POST.get('query_ip'))
        queyruser = str_dos2unix(request.POST.get('query_user'))
        querypassw = str_dos2unix(request.POST.get('query_pass'))
        querypath = str_dos2unix(request.POST.get('query_path'))
        testtag = str_dos2unix(request.POST.get('testtag'))
        lan_sel = request.POST.get('lan_sel')
        fromto = request.POST.get('inlineRadioOptions')
        if fromto == 'tozh':
            fromlan = lan_sel
            tolan = 'zh-CHS'
        else:
            fromlan = 'zh-CHS'
            tolan = lan_sel

        try:
            models.ManEval.objects.create(create_time=get_now_time(), user=user_id, hubsvn=hubsvn,
                                         sersvn=sersvn,
                                         hubcfgip=hubcfgip, hubcfguser=hubcfguser,
                                         hubcfgpassw=hubcfgpassw, hubcfgpath=hubcfgpath, hubdatapath=hubdatapath,
                                         sercfgip=sercfgip, sercfguser=sercfguser, sercfgpassw=sercfgpassw,
                                         sercfgpath=sercfgpath, serdatapath=serdatapath, queryip=queryip,
                                         queyruser=queyruser,
                                         querypassw=querypassw, querypath=querypath,
                                         testtag=testtag, fromlan=fromlan, tolan=tolan, lan_sel=lan_sel,
                                         isfromzh=fromto)
        except Exception as e:
            print(e)
            ret['error'] = 'error:' + str(e)
            ret['status'] = False
        return HttpResponse(json.dumps(ret))

# monitor
@auth
def gpu_detail(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('taskid')
    task_detail = models.GpuMonitor.objects.filter(id=int(task_id))
    return render(request, 'fanyi/gpu_detail.html',{'user_id': user_id,'task_detail': task_detail})


def gpu_del_task(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('monitor_id')
    try:
        models.GpuMonitor.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))


def gpu_task_stop(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        running_pid = models.Host.objects.filter(id=req_id, status=1).values('runningPID')
        if running_pid:
            for item in running_pid:
                # os.popen('kill -9 %s' % item['runningPID'])
                os.kill(int(item['runningPID']), signal.SIGTERM)
        models.Host.objects.filter(id=req_id).update(runningPID="", status=0)
        models.GpuMonitor.objects.filter(status=1, h_id=req_id).update(status=0, end_time=get_now_time())
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))


@auth
def gpu_task_start(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        running_pid = models.Host.objects.filter(id=req_id, status=1).values('runningPID')
        print(running_pid)
        monitor_ip = models.Host.objects.filter(id=req_id).first()

        if running_pid:
            for item in running_pid:
                os.kill(int(item['runningPID']), signal.SIGTERM)
        close_all_id = models.GpuMonitor.objects.filter(status=1, h_id=req_id).values('id')
        for close_id in close_all_id:
            models.GpuMonitor.objects.filter(id=close_id['id'], h_id=req_id).update(status=0)
        models.GpuMonitor.objects.create(create_time=get_now_time(), monitorip=monitor_ip.ip, user=user_id, status=1, h_id=req_id)
        running_case_id = models.GpuMonitor.objects.filter(status=1, h_id=req_id).first()
        print('running_case_id',running_case_id)
        print('req_id',req_id)
        os.system('/usr/local/bin/python3 /search/odin/pypro/webqa/utils/monitor.py %s %s &' % (str(running_case_id.id),req_id))
        time.sleep(1)
        new_running_ip = models.Host.objects.filter(id=req_id).first()
        if new_running_ip.runningPID == '':
            ret['status'] = False
            ret['error'] = "Error:start error"
            models.GpuMonitor.objects.filter(id=running_case_id.id).update(status=2)
    except Exception as e:
        print(e)
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))


def gpu_del_host(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        models.Host.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))


@auth
def gpu(request):
    # uid = 'zhangjingjun'
    uid = request.COOKIES['uid']
    if request.method == 'GET':
        page = request.GET.get('page')
        task_id = request.GET.get('taskid')
        if task_id is None or task_id == 'None':
            task_id = ''
        current_page = 1
        if page:
            current_page = int(page)
        try:
            if task_id == '':
                gpu_info = models.GpuMonitor.objects.filter(user=uid).values('id', 'create_time', 'end_time', 'monitorip', 'user', 'status').order_by('id')[::-1]
            else:
                gpu_info = models.GpuMonitor.objects.filter(h_id=task_id,user=uid).values('id', 'create_time', 'end_time', 'monitorip', 'user', 'status').order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(gpu_info), 15, 9)
            data = gpu_info[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/fanyi/gpu/?taskid=%s&page=" % task_id)

            host_list = models.Host.objects.filter(user_fk_id=uid).order_by('ip')
        except Exception as e:
            print(e)
            pass
        return render(request, 'fanyi/gpu_monitor.html', {'user_id': uid, 'li': data, 'page_str': page_str, 'host_list': host_list})
    elif request.method == 'POST':
        ret = {'status': True, 'errro': None, 'data': None}
        ip = request.POST.get('monitorip')
        monitor_user = request.POST.get('monitoruser')
        monitor_passw = request.POST.get('monitorpassw')
        gpuid = request.POST.get('gpuid')
        if gpuid == '':
            gpuid = 0
        try:
            nameisExist = models.Host.objects.filter(ip=ip, gpuid=gpuid)
            if nameisExist.exists() == False:
                models.Host.objects.create(ip=ip, user=monitor_user, passw=monitor_passw, gpuid=int(gpuid),user_fk_id=uid)
            else:
                ret['error'] = "Error:ip已存在，请勿重新添加"
                ret['status'] = False
        except Exception as e:
            ret['error'] = "Error:" + str(e)
            print(e)
            ret['status'] = False
        return HttpResponse(json.dumps(ret))


# bbk
@auth
def bbk(request):
    # uid = 'zhangjingjun'
    uid = request.COOKIES['uid']
    if request.method == 'GET':
        page = request.GET.get('page')
        current_page = 1
        if page:
            current_page = int(page)
        try:
            req_list = models.ReqInfo.objects.filter(user_fk_id=uid).order_by('id')[::-1]
            req_list = models.ReqInfo.objects.order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(req_list), 5, 5)
            data = req_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/fanyi/bbk?page=")
        except Exception as e:
            print(e)
            pass
        return render(request, 'fanyi/bbk.html', {'user_id': uid, 'li': data, 'page_str': page_str})
    elif request.method == 'POST':
        ret = {'status': True, 'errro': None, 'data': None}
        inputHost = request.POST.get('inputHost')
        reqtype = request.POST.get('reqtype')
        lan_sel = request.POST.get('lan_sel')
        fromto = request.POST.get('inlineRadioOptions')
        reqtext = request.POST.get('reqtext')
        if fromto == 'tozh':
            fromlan = lan_sel
            tolan = 'zh-CHS'
        else:
            fromlan = 'zh-CHS'
            tolan = lan_sel
        try:
            threads = []
            # Sogou
            t_sg = sogofy_t.sgThread(target=sogofy_t.getResult_sg,args=(inputHost,fromlan,tolan,reqtext,reqtype))
            threads.append(t_sg)
            # Baidu
            t_bd = baidufy_t.bdThread(target=baidufy_t.getResult_bd, args=(fromlan, tolan, reqtext))
            threads.append(t_bd)
            # google 接口失效
            # t_gg = googlefy_t.ggThread(target=googlefy_t.getResult_gg, args=(fromlan, tolan, reqtext))
            # threads.append(t_gg)
            # QQ
            t_qq = qqfy_t.qqThread(target=qqfy_t.getResult_qq, args=(fromlan, tolan, reqtext))
            threads.append(t_qq)
            # youdao
            t_yd = youdaofy_t.ydThread(target=youdaofy_t.getResult_yd, args=(fromlan, tolan, reqtext))
            threads.append(t_yd)

            for thead_id in range(len(threads)):
                threads[thead_id].start()
            sg_result = threads[0].join()
            if sg_result['status'] is False:
                ret['status'] = False
                ret['error'] = sg_result['error']
            else:
                ret['transResult'] = sg_result['data']
            ret['bd_result'] = threads[1].join()
            # ret['gg_result'] = threads[1].join()
            ret['qq_result'] = threads[2].join()
            ret['yd_result'] = threads[3].join()
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


# debug and bbk del
def del_line(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        models.ReqInfo.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))


@auth
def req_info_save(request):
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
    # uid = 'zhangjingjun'
    uid = request.COOKIES['uid']
    if request.method == 'GET':
        page = request.GET.get('page')
        current_page = 1
        if page:
            current_page = int(page)
        try:
            req_list = models.ReqInfo.objects.filter(user_fk_id=uid).order_by('id')[::-1]
            req_list = models.ReqInfo.objects.order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(req_list), 12, 5)
            data = req_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/fanyi/debug?page=")
        except Exception as e:
            print(e)
            pass
        return render(request, 'fanyi/debug.html',{'user_id': uid,'li': data,'page_str': page_str})
    elif request.method == 'POST':
        ret = {'status': True, 'errro': None, 'data': None}
        inputHost = request.POST.get('inputHost')
        reqtype = request.POST.get('reqtype')
        lan_sel = request.POST.get('lan_sel')
        fromto = request.POST.get('inlineRadioOptions')
        reqtext = request.POST.get('reqtext')
        if fromto == 'tozh':
            fromlan = lan_sel
            tolan = 'zh-CHS'
        else:
            fromlan = 'zh-CHS'
            tolan = lan_sel
        try:
            t_sg = sogofy_t.getResult_sg(inputHost, fromlan, tolan, reqtext, reqtype)
            if t_sg['status'] is False:
                ret['status'] = False
                ret['error'] = t_sg['error']
            else:
                ret['transResult'] = t_sg['data']
                ret['debugInfo'] = t_sg['debugInfo']
                ret['requestStr'] = t_sg['requestStr']
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


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')


def str_unix2br(input):
    return input.replace('\n', '<br>')
