from django.shortcuts import render, redirect, HttpResponse
from publicEnv import models
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


# @auth
def if_eval_detail(request):
    user_id="zhangjingjun"
    # user_id = request.COOKIES.get('uid')
    task_id = request.GET.get('svid')
    task_detail = models.ServiceStatus.objects.filter(id=task_id).first()
    return render(request, 'fanyi/if_eval_detail.html',{'user_id': user_id, 'task_detail': task_detail})

@auth
def svcheck(request):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    if request.method == 'GET':
        page = request.GET.get('page')
        current_page = 1
        if page:
            current_page = int(page)
        try:
            task_list = models.ServiceStatus.objects.order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(task_list), 16, 9)
            data = task_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/publicsv/svcheck?page=")
        except Exception as e:
            print(e)
            pass
        return render(request, 'publicsv/svcheck.html', {'user_id': user_id, 'li': data, 'page_str': page_str})