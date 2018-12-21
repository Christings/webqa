from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from utils import pagination
import json, os, time

from rest_framework import viewsets
from rest_framework.views import Response
from ml.utils.serializers import *
from ml.models import Project, Rule, Field, update_crawl_template
from ml.utils.template_engine import generate_crawl
from ml.utils.utils import create_md5


# Create your views here.

def auth(func):
    def inner(request, *args, **kwargs):
        login_url = "https://login.sogou-inc.com/?appid=1220&sso_redirect=http://webqa.web.sjs.ted/login&targetUrl="
        # try:
        #     user_id = request.COOKIES.get('uid')
        #     if not user_id:
        #         return redirect(login_url)
        # except:
        #     return redirect(login_url)
        return func(request, *args, **kwargs)

    return inner

# @csrf_exempt
# def crawler_list(request):
#     queryset = Project.objects.all()
#
#     return render(request, "publicsv/crawler.html", {"project": queryset})


def crawler_add(request):
    return render(request, "ml/crawler_add.html")


class ProjectViewSet(viewsets.ViewSet):
    user_id = 'gongyanli'

    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

    def list(self, request):
        # public_projects = self.queryset.filter(is_public=True, is_delete=False)
        projects = self.queryset.all()

        return render(request, 'ml/crawler.html', {"project": projects})

    # def retrieve(self, request, pk=None):
    #     user_id = 'gongyanli'
    #     queryset = self.queryset.filter(id=pk)
    #     queryset = queryset[0] if queryset else None
    #     if not queryset:
    #         return JsonResponse({"msg": "project not found"})
    #     if queryset.is_public or queryset.user == user_id:
    #         serializer = ProjectDetailSerializer(queryset)
    #         if queryset.is_public:
    #             render_template = "ml/crawler.html"
    #         else:
    #             render_template = "ml/crawler_detail.html"
    #         return render(request, render_template, {"project": serializer.data})
    #     return JsonResponse({"msg": "project not found"})

    def create(self, request):
        user_id = 'gongyanli'

        data = request.data.copy()
        data["user"] = user_id
        data["md5"] = create_md5()
        data["status"] = 1
        serializer = ProjectDetailSerializer(data=data)
        if serializer.is_valid():
            print('success')
            project = serializer.create(data)
            update_crawl_template(project)
            return Response({"msg": "ok", "id": project.id})
        return Response(serializer.errors)

    def update(self, request, pk=None):
        user_id = 'gongyanli'
        # queryset = self.queryset.filter(id=pk, user=request.user)
        queryset = self.queryset.filter(id=pk, user=user_id)
        queryset = queryset[0] if queryset else None
        if not queryset:
            return Response({"msg": "project not found"})
        data = request.data.copy()
        # data["user"] = request.user
        data["user"] = request.user_id
        serializer = ProjectDetailSerializer(queryset, data=data)
        if serializer.is_valid():
            instance = serializer.update(queryset, data)
            update_crawl_template(instance)
            return Response({"msg": "ok", "data": {"id": instance.id}})
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        user_id = 'gongyanli'
        project = Project.objects.get(pk=pk, user=user_id)
        # project = Project.objects.get(pk=pk, user=user_id)
        # project.is_delete = True
        # project.save()
        project.delete()
        return Response({"msg": "ok"})


def crawler_detail(request, id):
    user_id = 'gongyanli'

    if request.method == "GET":
        print('get')
        project = get_object_or_404(Project,pk=id)
        return render(request, "ml/crawler_detail.html", {"project": project})
    if request.method == "POST":
        user = user_id
        body = json.loads(request.body)
        id = body.get("id")
        status = int(body.get("status", 0))
        project = Project.objects.get(pk=id,user=user)
        project.status = status
        project.save()

        rule_fields = []
        rules = Rule.objects.filter(project=project)
        for rule in rules:
            fields = Field.objects.filter(rule=rule)
            rule_fields.append({"rule": rule, "field": fields})

        if status == 1:
            generate_crawl(project, rule_fields)
        return JsonResponse({"msg": "ok"})
    return JsonResponse({'msg': "method not allowed"})


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

    def create(self, request):
        serializer = RuleSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"msg": "ok", "data": {"id", instance.id}})
        return Response(serializer.errors)

    def destory(self, request, pk=None):
        Rule.objects.filter(pk=pk).delete()
        return Response({"msg": "ok"})


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def create(self, request):
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"msg": "ok", "data": {"id", instance.id}})
        return Response(serializer.errors)

    def destory(self, request, pk=None):
        Field.objects.filter(pk=pk).delete()
        return Response({"msg": "ok"})


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def str_unix2br(input):
    return input.replace('\n', '<br>')
