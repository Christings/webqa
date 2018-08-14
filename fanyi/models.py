from django.db import models

# Create your models here.
class ReqInfo(models.Model):
    host_ip = models.CharField(max_length=128)
    trans_direct = models.CharField(max_length=20)
    isfromzh = models.CharField(max_length=10)
    req_text = models.CharField(max_length=2000)
    result = models.CharField(max_length=2000)
    user_fk = models.ForeignKey(to='UserInfo',to_field='user_name',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now=True)
    reqtype = models.CharField(max_length=20)