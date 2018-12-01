from django.shortcuts import render, redirect, HttpResponse
from collections import Counter
from publicEnv import models
from django.db.models import Q
from utils import pagination
import json,re
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
        return func(request,*args,**kwargs)
    return inner

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
            urllist = models.Special_check_deadlink.objects.using('db_fhz').values('url')
            url_list = list()
            for url in  urllist:
                result = re.findall(".*//(.*?)/.*", url['url'])
                if result:
                    url_list.append(result[0])
            list30 = Counter(url_list).most_common(30)
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
