from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from fanyi import models as layout
from rbac import models
from wiki import models
from django.db.models import Q
from utils import pagination
from utils import resizeImg
import json, time, markdown2, os
from django.views.decorators.csrf import csrf_exempt
from .forms import EditorTestForm
from django.http import JsonResponse


# Create your views here.

def auth(func):
    def inner(request, *args, **kwargs):
        # login_url = "https://login.sogou-inc.com/?appid=1162&sso_redirect=http://frontqa.web.sjs.ted/&targetUrl="
        # try:
        #     user_id = request.COOKIES.get('uid')
        #     if not user_id:
        #         return redirect(login_url)
        # except:
        #     return redirect(login_url)
        # v = request.COOKIES.get('username111')
        return func(request, *args, **kwargs)

    return inner


# wiki detail
@auth
def wiki_detail(request, task_id):
    # user_id = 'zhangjingjun'
    user_id = request.COOKIES.get('uid')
    try:
        req_lst = layout.ReqInfo.objects.filter(user_fk_id=user_id)
        app_id_lst = list()

        wikidetail = models.Wiki.objects.filter(id=task_id).values()
        format_md = markdown2.markdown(wikidetail[0]['content'])

        wikitags = models.Wiki.objects.filter(id=task_id).values('tag')
        taglist = list()
        for item in wikitags:
            if '--' in item['tag']:
                tagsp = item['tag'].split('--')
                taglist += tagsp
            else:
                taglist.append(item['tag'])
        taglist = list(set(taglist))

    except Exception as e:
        print(e)
        pass
    return render(request, 'wiki/wiki_detail.html',
                  {'user_id': user_id,
                   'req_lst': req_lst,
                   'wikidetail': wikidetail, 'format_md': format_md, 'taglist': taglist})


# del wiki
@csrf_exempt
@auth
def del_wiki(request):
    # user_id = 'zhangjingjun'
    ret = {'status': True, 'error': None, 'data': None}
    req_id = request.POST.get('line_id')
    try:
        # models.Wiki.objects.filter(id=req_id).update(status=2)
        models.Wiki.objects.filter(id=req_id).delete()
    except Exception as e:
        ret['status'] = False
        ret['error'] = "Error:" + str(e)
    return HttpResponse(json.dumps(ret))


def wiki(request, page_id='1'):
    if page_id == '':
        page_id = 1
    if request.method == "GET":
        # form = EditorTestForm(instance=b)
        tag = request.GET.get('tag')
        category = request.GET.get('category')

        if tag and category == None:
            # data = models.Wiki.objects.filter(tag=tag)
            data = models.Wiki.objects.filter(Q(tag__icontains=tag)) # 模糊查询

            return render(request, 'wiki/wiki.html',
                          {'form': data})
        elif tag == None and category:
            data = models.Wiki.objects.filter(category=category)

            return render(request, 'wiki/wiki.html',
                          {'form': data})
        elif tag == None and category == None:
            wiki_list = models.Wiki.objects.all()
            category_list = models.Wiki.objects.values('category').distinct()
            taglist = models.Wiki.objects.values('tag').distinct()

            tag_list = list()
            for item in taglist:
                if ',' in item['tag']:
                    tag_list += item['tag'].split(',')
                else:
                    tag_list.append(item['tag'])
            tag_list = list(set(tag_list))

            current_page = int(page_id)
            page_obj = pagination.Page(current_page, len(wiki_list), 10, 9)
            data = wiki_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str('/wiki/wiki')
            return render(request, 'wiki/wiki.html',
                          {'form': data, 'page_str': page_str, 'category_list': category_list, 'tag_list': tag_list})


def edit_wiki(request):
    user_id = 'gongyanli'
    # user_id=request.COOKIES.get('uid')
    edit_id = request.GET.get('id')
    # b = models.UserInfo.objects.filter(user_fk_id=user_id)
    edit_content = models.Wiki.objects.get(id=edit_id)

    if request.method == "GET":
        form = EditorTestForm(instance=edit_content)
        return render(request, 'wiki/wiki_add.html', {'form': form})
    if request.method == "POST":
        form = EditorTestForm(request.POST, instance=edit_content)
        if form.is_valid():
            wiki = form.save(commit=False)
            # form.title = request.POST.get('title')
            wiki.update_time = get_now_time()
            wiki.update_user = user_id
            wiki.save()
            return HttpResponseRedirect('wiki/')

            # return JsonResponse(dict(success=1, message="submit success!"))
        else:
            return JsonResponse(dict(success=0, message="submit error"))


def add_wiki(request):
    user_id = 'gongyanli'
    # user_id = request.COOKIES.get('uid')
    if request.method == "POST":
        obj = models.Wiki.objects.create(user=user_id, create_time=get_now_time(), update_time=get_now_time())
        form = EditorTestForm(request.POST, instance=obj)

        if form.is_valid():
            # form.save()
            xx = form.save(commit=False)
            # xx.save()
            xx.user = user_id
            xx.create_time = get_now_time()
            xx.save()
            form.save_m2m()
            return HttpResponseRedirect('wiki/')
            # return render(request, 'wiki/wiki_list.html', {'form': form})
            # return JsonResponse(dict(success=1, message="submit success!"))
        else:
            return JsonResponse(dict(success=0, message="submit error"))
    else:
        form = EditorTestForm()
        return render(request, 'wiki/wiki_add.html', {'form': form})


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
