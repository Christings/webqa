from django.shortcuts import render,redirect
# from mleval import models
import time
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

# @auth
def gpu_detail(request):
    user_id = 'zhangjingjun'
    # user_id = request.COOKIES.get('uid')
    # task_id = request.GET.get('taskid')
    return render(request, 'mleval/gpu_detail.html',{'user_id': user_id})


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')


def str_unix2br(input):
    return input.replace('\n', '<br>')