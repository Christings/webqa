from django.db import models
from rbac.models import UserInfo
# Create your models here.

class ReqInfo(models.Model):
    host_ip = models.CharField(max_length=128)
    trans_direct = models.CharField(max_length=20)
    isfromzh = models.CharField(max_length=10)
    req_text = models.TextField(default="")
    oriresult = models.CharField(max_length=2000)
    result = models.CharField(max_length=2000,default="")
    user_fk = models.ForeignKey(to=UserInfo,to_field='username',on_delete=models.CASCADE)
    reqtype = models.CharField(max_length=20)
    reqfield = models.CharField(max_length=20,default="")
    json_chn_query = models.CharField(max_length=256,default="")


class Host(models.Model):
    ip = models.GenericIPAddressField()
    user = models.CharField(max_length=500, default="")
    passw = models.CharField(max_length=500, default="")
    status = models.IntegerField(default=0)
    runningPID = models.CharField(max_length=20, default="")
    gpuid = models.IntegerField(default=0)
    processname = models.TextField(default="")
    user_fk = models.ForeignKey(to=UserInfo, to_field='username', on_delete=models.CASCADE)


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
    gpumem_list = models.TextField(default="")
    gpumemused_list = models.TextField(default="")
    gpuid = models.IntegerField(default=0)
    errorlog = models.TextField(default="")
    h = models.ForeignKey(to="Host", to_field='id', on_delete=models.CASCADE)


class ManEval(models.Model):
    create_time = models.CharField(max_length=50, default="")
    start_time = models.CharField(max_length=50, default="")
    end_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    hubcfgip = models.CharField(max_length=500, default="")
    hubcfguser = models.CharField(max_length=500, default="")
    hubcfgpassw = models.CharField(max_length=500, default="")
    hubcfgpath = models.CharField(max_length=500, default="")
    hubdatapath = models.CharField(max_length=500, default="")
    sercfgip = models.CharField(max_length=500, default="")
    sercfguser = models.CharField(max_length=500, default="")
    sercfgpassw = models.CharField(max_length=500, default="")
    sercfgpath = models.CharField(max_length=500, default="")
    serdatapath = models.CharField(max_length=500, default="")
    queryip = models.CharField(max_length=500, default="")
    queyruser = models.CharField(max_length=500, default="")
    querypassw = models.CharField(max_length=500, default="")
    querypath = models.CharField(max_length=500, default="")
    runningIP = models.CharField(max_length=50, default="")
    hubsvn = models.TextField(default="")
    sersvn = models.TextField(default="")
    errorlog = models.TextField(default="")
    testtag = models.CharField(max_length=500, default="")
    finished = models.IntegerField(default=0)
    diffnum = models.IntegerField(default=0)
    fromlan = models.CharField(max_length=20, default="")
    tolan = models.CharField(max_length=20, default="")
    isfromzh = models.CharField(max_length=10, default="")
    lan_sel = models.CharField(max_length=10, default="")


class ManEvalDiff(models.Model):
    create_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50)
    diff_content = models.TextField(default="")
    diff_task = models.ForeignKey(to="ManEval", to_field='id', on_delete=models.CASCADE)


