"""webqa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import include, re_path
from django.views.generic.base import RedirectView
from fanyi import views

urlpatterns = [
    re_path(r'favicon.ico', RedirectView.as_view(url=r'static/favicon.ico')),
    re_path('admin/', admin.site.urls),
    re_path(r'^$', views.login),
    re_path(r'login/', views.login),
    re_path(r'logout/', views.logout),
    re_path(r'index/', views.index),
    re_path(r'rbac/', include('rbac.urls')),
    re_path(r'polls/', include('polls.urls')),
    re_path(r'fanyi/', include('fanyi.urls')),
    re_path(r'webqo/', include('webqo.urls')),
    re_path(r'webqw/', include('webqw.urls')),
    re_path(r'wiki/', include('wiki.urls')),
    re_path(r'publicsv/', include('publicEnv.urls')),
    #re_path(r'ml/', include('ml.urls')),
    # re_path(r'^$', RedirectView.as_view(url='/project')),

    re_path(r'', include('editor_md.urls')),
    re_path(r"^static/media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),


]
