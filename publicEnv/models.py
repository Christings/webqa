from django.db import models

# Create your models here.
class ServiceStatus(models.Model):
    sv_name = models.CharField(max_length=100, default="")
    sv_host = models.CharField(max_length=50, default="")
    sv_port = models.CharField(max_length=10, default="")
    sv_port_type = models.IntegerField(default=0)
    svninfo = models.TextField(default="")
    update_time = models.CharField(max_length=50, default="")
    status = models.IntegerField(default=0)
    sv_path = models.CharField(max_length=500, default="")
    host_online = models.CharField(max_length=50, default="")
    path_online = models.CharField(max_length=500, default="")
