from django.db import models
from editor_md.models import EditorMdField, EditorMdWidget, AdminEditorMdWidget


# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Wikistore(models.Model):
    create_time = models.CharField(max_length=50, default="")
    update_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50, default="")
    update_user = models.CharField(max_length=50, default="")
    status = models.IntegerField(default=0)
    wikititle = models.CharField(max_length=200, default="")
    wikisummary = models.CharField(max_length=400, default="")
    # wikicontent = models.TextField(default="")
    wikicontent = EditorMdField(imagepath="editor_md_image/", default="")
    # wikicontent = AdminEditorMdWidget(AdminEditorMdWidget,EditorMdWidget)
    wikitag = models.CharField(max_length=200, default="")

    # category = models.ForeignKey(to='Category', on_delete=models.CASCADE, to_field='id',default='')
    # tags = models.ManyToManyField(Tag, blank=True)
    category = models.CharField(max_length=100, default='')
    # tags = models.ManyToManyField(Tag, blank=True)
