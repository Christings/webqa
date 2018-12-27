from django.shortcuts import redirect

def auth(func):
    def inner(request,*args,**kwargs):
        login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/login&targetUrl="
        try:
            user_id = request.COOKIES.get('uid')
            if not user_id:
                return redirect(login_url)
        except:
            return redirect(login_url)
        return func(request,*args,**kwargs)
    return inner


publicPem_path='/search/odin/pypro/webqa/public.pem'

login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/login&targetUrl="

