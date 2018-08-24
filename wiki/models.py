from django.db import models
# Create your models here.

class Wikistore(models.Model):
    create_time = models.CharField(max_length=50, default="")
    update_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50, default="")
    update_user= models.CharField(max_length=50, default="")
    status = models.IntegerField(default=0)
    wikititle = models.CharField(max_length=200, default="")
    wikisummary = models.CharField(max_length=400,default="")
    wikicontent = models.TextField(default="")
    wikitag = models.CharField(max_length=200, default="")
