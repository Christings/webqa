from django.db import models
import django.utils.timezone as timezone
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
