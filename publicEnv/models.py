from django.db import models
from rbac.models import UserInfo
# Create your models here.
class ServiceStatus(models.Model):
    sv_name = models.CharField(max_length=100, default="")
    sv_host = models.CharField(max_length=50, default="")
    sv_port = models.CharField(max_length=10, default="")
    sv_port_type = models.IntegerField(default=0)
    svninfo = models.TextField(default="")
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    sv_path = models.CharField(max_length=500, default="")
    host_online = models.CharField(max_length=50, default="")
    path_online = models.CharField(max_length=500, default="")

class ServiceSt(models.Model):
    sv_name = models.CharField(max_length=100, default="")
    sv_host = models.CharField(max_length=50, default="")
    sv_port = models.CharField(max_length=10, default="")
    sv_port_type = models.IntegerField(default=0)
    svninfo = models.TextField(default="")
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=False)
    status = models.IntegerField(default=0)
    sv_path = models.CharField(max_length=500, default="")
    host_online = models.CharField(max_length=50, default="")
    path_online = models.CharField(max_length=500, default="")


class Special_check_deadlink(models.Model):
    url = models.CharField(max_length=255, null=False)
    imgurl = models.CharField(max_length=255, null=False)
    add_timestamp = models.DateTimeField(auto_now=True, null=False)
    error_count = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    vrid = models.IntegerField(default=0)
    last_timestamp = models.DateTimeField(auto_now_add=True, null=False)
    status_code = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    comment = models.TextField(default="")
    query = models.CharField(max_length=50, default='')
    ua_type = models.IntegerField(default=0)
    vr_name = models.CharField(max_length=255, default='')
    principal = models.CharField(max_length=255, default='')
    re_check_fail = models.IntegerField(default=0)
    manual_pass = models.IntegerField(default=0)
    uuid = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'special_check_deadlink'
        ordering = ['-error_count']


class AnalyDetail(models.Model):
    create_time = models.CharField(max_length=50, default="")
    end_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    ip = models.CharField(max_length=500, default="")
    user = models.CharField(max_length=500, default="")
    passw = models.CharField(max_length=500, default="")
    testlog_path=models.CharField(max_length=500, default="")
    testp = models.CharField(max_length=10, default="")
    test_interval = models.CharField(max_length=10, default="")
    baselog_path=models.CharField(max_length=500, default="")
    basep = models.CharField(max_length=10, default="")
    base_interval = models.CharField(max_length=10, default="")
    testres_list = models.TextField(default="")
    baseres_list = models.TextField(default="")
    errorlog = models.TextField(default="")
    user_fk = models.ForeignKey(to=UserInfo, to_field='username', default="", on_delete=models.CASCADE)