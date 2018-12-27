from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from fanyi import models as layout
from rbac import models
from wiki import models
from django.db.models import Q
from utils import pagination
from utils import resizeImg
import json, time, os
from django.views.decorators.csrf import csrf_exempt
from .forms import EditorTestForm
from django.http import JsonResponse
from utils.verify import auth

# Create your views here.


# wiki detail
def wiki_detail(request, task_id):
    try:
        info = models.Wiki.objects.filter(id=task_id)

        b = models.Wiki.objects.get(id=task_id)
        form = EditorTestForm(instance=b)

        wikitags = models.Wiki.objects.filter(id=task_id).values('tag')
        taglist = list()
        for item in wikitags:
            if ',' in item['tag']:
                tagsp = item['tag'].split(',')
                taglist += tagsp
            else:
                taglist.append(item['tag'])
        taglist = list(set(taglist))

        return render(request, 'wiki/wiki_detail.html',
                      {'form': form, 'taglist': taglist, 'info': info})
    except Exception as e:
        print(e)
        pass


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

def wiki(request):
    if request.method == "GET":
        page = request.GET.get('page')
        # form = EditorTestForm(instance=b)
        tag = request.GET.get('tag')
        category = request.GET.get('category')
        current_page = 1
        if page:
            current_page = int(page)
        if tag and category == None:
            wiki_list = models.Wiki.objects.filter(Q(tag__icontains=tag)).order_by('-update_time')  # 模糊查询
        elif tag == None and category:
            wiki_list = models.Wiki.objects.filter(category=category).order_by('-update_time')
        else:
            wiki_list = models.Wiki.objects.all().order_by('-update_time')

        category_list = models.Wiki.objects.values('category').distinct()
        taglist = models.Wiki.objects.values('tag').distinct()
        tag_list = list()
        for item in taglist:
            if ',' in item['tag']:
                item['tag']=item['tag'].replace('，',',')
                tag_list += item['tag'].split(',')
            else:
                tag_list.append(item['tag'])
        tag_list = list(set(tag_list))
        page_obj = pagination.Page(current_page, len(wiki_list), 18, 9)
        data = wiki_list[page_obj.start:page_obj.end]
        page_str = page_obj.page_str('/wiki/wiki?page=')
        return render(request, 'wiki/wiki.html',{'form': data, 'page_str': page_str, 'category_list': category_list, 'tag_list': tag_list})


@auth
def edit_wiki(request):
    # user_id = 'gongyanli'
    user_id = request.COOKIES.get('uid')
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
            return HttpResponseRedirect('/wiki/wiki/')

            # return JsonResponse(dict(success=1, message="submit success!"))
        else:
            return JsonResponse(dict(success=0, message="submit error"))


@auth
def add_wiki(request):
    # user_id = 'gongyanli'
    user_id = request.COOKIES.get('uid')
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
            return HttpResponseRedirect('/wiki/wiki/')
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
