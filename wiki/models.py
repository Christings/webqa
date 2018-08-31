from django.db import models
from editor_md.models import EditorMdField, EditorMdWidget, AdminEditorMdWidget


class Wiki(models.Model):
    create_time = models.CharField(max_length=50, default="")
    update_time = models.CharField(max_length=50, default="")
    user = models.CharField(max_length=50, default="")
    update_user = models.CharField(max_length=50, default="")

    title = models.CharField(max_length=200, default="")
    content = EditorMdField(imagepath="editor_md_image/", default="")
    category = models.CharField(max_length=100, default='')
    tag = models.CharField(max_length=200, default="")

    # category = models.ForeignKey(to='Category', on_delete=models.CASCADE, to_field='id',default='')
    # tags = models.ManyToManyField(Tag, blank=True)
