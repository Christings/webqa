# -*- coding: utf-8 -*-
# __author__ = "gongyanli"
from __future__ import unicode_literals, print_function, division
from django import forms
from django.forms import TextInput
from .models import Wiki


class EditorTestForm(forms.ModelForm):
    class Meta:
        model = Wiki
        fields = ("title", "category", "tag", "content")
        labels = {'title': '', 'tag': '', 'content': '', 'category': ''}
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control', 'placeholder': '标题', 'style': 'width:86%;margin:0 0 0 7%'}),
            'category': TextInput(
                attrs={'class': 'form-control', 'placeholder': '分类', 'style': 'width:86%;margin:0 0 0 7%'}),
            'tag': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'tag1,tag2,tag3', 'style': 'width:86%;margin:0 0 0 7%'}),
        }
