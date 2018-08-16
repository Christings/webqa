from django.db import models
from rbac.models import UserInfo
# Create your models here.

class ReqInfo(models.Model):
    host_ip = models.CharField(max_length=128)
    trans_direct = models.CharField(max_length=20)
    isfromzh = models.CharField(max_length=10)
    req_text = models.CharField(max_length=2000)
    result = models.CharField(max_length=2000)
    user_fk = models.ForeignKey(to=UserInfo,to_field='username',on_delete=models.CASCADE)
    reqtype = models.CharField(max_length=20)


class Host(models.Model):
    ip = models.GenericIPAddressField(db_index=True)
    user = models.CharField(max_length=500, default="")
    passw = models.CharField(max_length=500, default="")
    status = models.IntegerField(default=0)
    runningPID = models.CharField(max_length=20, default="")
    gpuid = models.IntegerField(default=0)


class GpuMonitor(models.Model):
    create_time = models.CharField(max_length=50, default="")
    end_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    monitorip = models.CharField(max_length=500, default="")
    monitoruser = models.CharField(max_length=500, default="")
    monitorpassw = models.CharField(max_length=500, default="")
    gpumem = models.TextField(default="")
    gpumemused = models.TextField(default="")
    h = models.ForeignKey(to="Host", to_field='id', on_delete=models.CASCADE)


