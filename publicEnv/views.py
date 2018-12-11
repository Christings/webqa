from django.shortcuts import render, redirect, HttpResponse
from publicEnv import models
from django.db.models import Q
from utils import pagination
import json, os, time
# Create your views here.

def auth(func):
    def inner(request,*args,**kwargs):
        login_url = "https://login.sogou-inc.com/?appid=1220&sso_redirect=http://webqa.web.sjs.ted/login&targetUrl="
        try:
            user_id = request.COOKIES.get('uid')
            if not user_id:
                return redirect(login_url)
        except:
            return redirect(login_url)
        return func(request, *args, **kwargs)
    return inner

# @auth
def pnine_detail(request):
    user_id="zhangjingjun"
    # user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('taskid')
    task_detail = models.AnalyDetail.objects.using('default').filter(id=task_id).first()
    return render(request, 'publicsv/pnine_detail.html',{'user_id': user_id, 'task_detail': task_detail})

# @auth
def pnine(request):
    uid = 'zhangjingjun'
    # uid = request.COOKIES['uid']
    if request.method == 'GET':
        page = request.GET.get('page')
        current_page = 1
        if page:
            current_page = int(page)
        try:
            gpu_info = models.AnalyDetail.objects.using('default').filter(user_fk_id=uid).values('id', 'create_time', 'end_time',
                                                                             'ip', 'user', 'status', 'passw', 'testlog_path', 'baselog_path',
                                                                             'testp','basep','test_interval','base_interval').order_by('-id')
            page_obj = pagination.Page(current_page, len(gpu_info), 15, 9)
            data = gpu_info[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/publicsv/p99/?page=")
        except Exception as e:
            print(e)
            pass
        return render(request, 'publicsv/pnine.html', {'user_id': uid, 'li': data, 'page_str': page_str})
    elif request.method == 'POST':
        ret = {'status': True, 'errro': None, 'data': None}
        ip = request.POST.get('analyip')
        monitor_user = request.POST.get('analyuser')
        monitor_passw = request.POST.get('analypassw')
        testlogpath = request.POST.get('testlogpath')
        baselogpath = request.POST.get('baselogpath')
        testp = request.POST.get('testp99')
        test_interval = request.POST.get('test_interval')
        basep = request.POST.get('basep99')
        base_interval = request.POST.get('base_interval')
        if not testlogpath:
            testlogpath=''
        if not baselogpath:
            baselogpath=''
        if not testp:
            testp='0.99'
        if not test_interval:
            test_interval='10'
        if not basep:
            basep='0.99'
        if not base_interval:
            base_interval='10'
        print(ip,monitor_user,monitor_passw,testlogpath,baselogpath,basep)
        try:
            a=models.AnalyDetail.objects.using('default').create(create_time=get_now_time(), ip=ip, user=monitor_user, passw=monitor_passw,
                                                               testlog_path=testlogpath, testp=testp, test_interval=test_interval,
                                                               baselog_path=baselogpath, basep=basep, base_interval=base_interval, user_fk_id=uid)
            os.system('/root/anaconda3/bin/python3 /search/odin/pypro/webqa/utils/syncfiles_test.py %d &' % a.id)
        except Exception as e:
            models.AnalyDetail.objects.using('default').filter(id=a.id).update(status=2,errlog='start failed')
            ret['error'] = "Error:" + str(e)
            print(e)
            ret['status'] = False
        return HttpResponse(json.dumps(ret))



def del_line(request):
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('task_id')
    print(req_id)
    try:
        models.Special_check_deadlink.objects.using('db_fhz').filter(id=req_id).update(status=1)
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))

@auth
def get_urllist(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        try:
            # urllist = models.Special_check_deadlink.objects.using('db_fhz').values('url')
            # url_list = list()
            # for url in  urllist:
            #     result = re.findall(".*//(.*?)/.*", url['url'])
            #     if result:
            #         url_list.append(result[0])
            # list30 = Counter(url_list).most_common(30)
            list30 = models.Special_check_deadlink.objects.using('db_fhz').values('url','error_count').order_by('-error_count')[0:50]
        except Exception as e:
            print(e)
            pass
        return render(request, "publicsv/deadlink_url.html", {'user_id': user_id,'urllist':list30 })


@auth
def deadlink(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        page = request.GET.get('page')
        pstatus = request.GET.get('pstatus')
        pfrom = request.GET.get('pfrom')
        httpcode = request.GET.get('httpcode')
        pclient = request.GET.get('pclient')
        search_content = request.GET.get('key')
        if search_content:
            search_content = search_content
        else:
            search_content = ""
        current_page = 1
        if page:
            current_page = int(page)
        try:
            if search_content  and search_content != '':
                page_count = models.Special_check_deadlink.objects.using('db_fhz').filter(url__icontains=search_content).count()
                page_obj = pagination.Page(current_page, page_count, 15, 15)
                data = models.Special_check_deadlink.objects.using('db_fhz').filter(url__icontains=search_content)[page_obj.start:page_obj.end]
                page_str = page_obj.page_str("/publicsv/deadlink?key=%s&page=" % search_content)
            elif pstatus is None and pfrom is None and httpcode is None and pclient is None:
                page_count = models.Special_check_deadlink.objects.using('db_fhz').all().count()
                page_obj = pagination.Page(current_page, page_count, 15, 15)
                data = models.Special_check_deadlink.objects.using('db_fhz').all()[page_obj.start:page_obj.end]
                page_str = page_obj.page_str("/publicsv/deadlink?page=")
            elif pstatus:
                page_count = models.Special_check_deadlink.objects.using('db_fhz').filter(status=pstatus).count()
                page_obj = pagination.Page(current_page, page_count, 15, 15)
                data = models.Special_check_deadlink.objects.using('db_fhz').filter(status=pstatus)[page_obj.start:page_obj.end]
                page_str = page_obj.page_str("/publicsv/deadlink?pstatus=%s&page=" % pstatus)
            elif pfrom:
                page_count = models.Special_check_deadlink.objects.using('db_fhz').filter(type=pfrom).count()
                page_obj = pagination.Page(current_page, page_count, 15, 15)
                data = models.Special_check_deadlink.objects.using('db_fhz').filter(type=pfrom)[page_obj.start:page_obj.end]
                page_str = page_obj.page_str("/publicsv/deadlink?pfrom=%s" % pfrom)
            elif httpcode:
                page_count = models.Special_check_deadlink.objects.using('db_fhz').filter(status_code=httpcode).count()
                page_obj = pagination.Page(current_page, page_count, 15, 15)
                data = models.Special_check_deadlink.objects.using('db_fhz').filter(status_code=httpcode)[page_obj.start:page_obj.end]
                page_str = page_obj.page_str("/publicsv/deadlink?httpcode=%s&page=" % httpcode)
            elif pclient:
                page_count = models.Special_check_deadlink.objects.using('db_fhz').filter(ua_type=pclient).count()
                page_obj = pagination.Page(current_page, page_count, 15, 15)
                data = models.Special_check_deadlink.objects.using('db_fhz').filter(ua_type=pclient)[page_obj.start:page_obj.end]
                page_str = page_obj.page_str("/publicsv/deadlink?pclient=%s&page=" % (pclient))
            # if pstatus is None and pfrom is None and httpcode is None and pclient is None:
            #     page_count = models.Special_check_deadlink.objects.using('db_fhz').all().count()
            #     page_obj = pagination.Page(current_page, page_count, 28, 9)
            #     data = models.Special_check_deadlink.objects.using('db_fhz').all()[page_obj.start:page_obj.end]
            #     page_str = page_obj.page_str("/publicsv/deadlink?page=")
            # else:
            #     page_count = models.Special_check_deadlink.objects.using('db_fhz').filter(status=pstatus,type=pfrom, status_code=httpcode,ua_type=pclient).count()
            #     print(page_count)
            #     page_obj = pagination.Page(current_page, page_count, 28, 9)
            #     data = models.Special_check_deadlink.objects.using('db_fhz').filter(status=pstatus, type=pfrom, status_code=httpcode, ua_type=pclient)[page_obj.start:page_obj.end]
            #     page_str = page_obj.page_str("/publicsv/deadlink?pstatus=%s&pfrom=%s&httpcode=%s&pclient=%s&page=" % (pstatus, pfrom, httpcode, pclient))

            httpcode_list = models.Special_check_deadlink.objects.using('db_fhz').raw('select distinct id ,status_code from special_check_deadlink group by status_code')
        except Exception as e:
            print(e)
            pass
        return render(request, "publicsv/deadlink.html", {'user_id': user_id,'li': data, 'page_str': page_str,'httpcode_list':httpcode_list})


@auth
def svcheck_detail(request):
    # user_id="zhangjingjun"
    user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('svid')
    task_detail = models.ServiceStatus.objects.using('default').filter(id=task_id).first()
    return render(request, 'publicsv/svcheck_detail.html',{'user_id': user_id, 'task_detail': task_detail})

@auth
def svcheck(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        tag = request.GET.get('tag')
        search_content = request.GET.get('key')
        page = request.GET.get('page')
        current_page = 1
        if page:
            current_page = int(page)
        if tag:
            tag = tag
        else:
            tag = ""
        if search_content:
            search_content = search_content
        else:
            search_content = ""
        try:
            if search_content  and search_content != '':
                task_list = models.ServiceStatus.objects.filter(
                    Q(sv_name__icontains=search_content) | Q(sv_host__icontains=search_content)
                    | Q(sv_port__icontains=search_content) | Q(svninfo__icontains=search_content)
                    | Q(sv_path__icontains=search_content) | Q(host_online__icontains=search_content)
                    | Q(path_online__icontains=search_content)).using('default').order_by('status')
            elif tag=='' or tag == 'all':
                task_list = models.ServiceStatus.objects.using('default').all().order_by('status')
            elif tag == 'crash':
                task_list = models.ServiceStatus.objects.using('default').filter(status=0).order_by('id')
            elif tag == 'unonline':
                task_list = models.ServiceStatus.objects.using('default').filter(host_online='').order_by('status')
            page_obj = pagination.Page(current_page, len(task_list), 28, 9)
            data = task_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/publicsv/svcheck?tag=%s&key=%s&page=" % (tag,search_content))
        except Exception as e:
            print(e)
            pass
        return render(request, 'publicsv/svcheck.html', {'user_id': user_id, 'li': data, 'page_str': page_str,'task_list':task_list})


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
