from django.shortcuts import render, redirect, HttpResponse
from publicEnv import models
from django.db.models import Q
from utils import pagination
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

def deadlink(request):
    # user_id = 'zhangjingjun'
    # user_id = request.COOKIES.get('uid')
    # if request.method == 'GET':
    #     page = request.GET.get('page')
    #     current_page = 1
    #     if page:
    #         current_page = int(page)
    #     try:
    #         task_list = models.InterfaceEval.objects.order_by('id')[::-1]
    #         page_obj = pagination.Page(current_page, len(task_list), 16, 9)
    #         data = task_list[page_obj.start:page_obj.end]
    #         page_str = page_obj.page_str("/fanyi/interface?page=")
    #     except Exception as e:
    #         print(e)
    #         pass
    #     return render(request, 'fanyi/interface.html', {'user_id': user_id, 'li': data, 'page_str': page_str})
    return render(request, 'publicsv/svcheck.html')


@auth
def svcheck_detail(request):
    # user_id="zhangjingjun"
    user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('svid')
    task_detail = models.ServiceStatus.objects.filter(id=task_id).first()
    return render(request, 'publicsv/svcheck_detail.html',{'user_id': user_id, 'task_detail': task_detail})

@auth
def svcheck(request):
    user_id = 'zhangjingjun'
    # user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        tag = request.GET.get('tag')
        search_content = request.GET.get('key')
        # try:
        #     if search_content is not None and search_content !='':
        #         task_list = models.ServiceStatus.objects.filter(
        #             Q(sv_name__icontains=search_content) | Q(sv_host__icontains=search_content)
        #             | Q(sv_port__icontains=search_content) | Q(svninfo__icontains=search_content)
        #             | Q(sv_path__icontains=search_content) | Q(host_online__icontains=search_content)
        #             | Q(path_online__icontains=search_content)).order_by('status')
        #     elif tag is None or tag == 'all':
        #         task_list = models.ServiceStatus.objects.all().order_by('status')
        #     elif tag == 'crash':
        #         task_list = models.ServiceStatus.objects.filter(status=0).order_by('id')
        #     elif tag == 'unonline':
        #         task_list = models.ServiceStatus.objects.filter(host_online='').order_by('status')
        # except Exception as e:
        #     print(e)
        #     pass
        # return render(request, 'publicsv/svcheck.html',{'user_id': user_id,'task_list': task_list})
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
        print('tag:',tag,' searchcount:',search_content,' page:',page)
        try:
            if search_content  and search_content != '':
                task_list = models.ServiceStatus.objects.filter(
                    Q(sv_name__icontains=search_content) | Q(sv_host__icontains=search_content)
                    | Q(sv_port__icontains=search_content) | Q(svninfo__icontains=search_content)
                    | Q(sv_path__icontains=search_content) | Q(host_online__icontains=search_content)
                    | Q(path_online__icontains=search_content)).order_by('status')
            elif tag=='' or tag == 'all':
                task_list = models.ServiceStatus.objects.all().order_by('status')
            elif tag == 'crash':
                task_list = models.ServiceStatus.objects.filter(status=0).order_by('id')
            elif tag == 'unonline':
                task_list = models.ServiceStatus.objects.filter(host_online='').order_by('status')
            page_obj = pagination.Page(current_page, len(task_list), 28, 9)
            data = task_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/publicsv/svcheck?tag=%s&key=%s&page=" % (tag,search_content))
        except Exception as e:
            print(e)
            pass
        return render(request, 'publicsv/svcheck.html', {'user_id': user_id, 'li': data, 'page_str': page_str,'task_list':task_list})
