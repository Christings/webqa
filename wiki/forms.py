# -*- coding: utf-8 -*-
# __author__ = "gongyanli"
from __future__ import unicode_literals, print_function, division
from django import forms
from django.forms import TextInput
from .models import Wikistore
from editor_md.models import EditorMdField, EditorMdWidget


# class EditorTestForm(forms.Form):
#     wikititle = forms.CharField()
#     wikicontent = EditorMdWidget()
#     wikitag = forms.CharField()


class EditorTestForm(forms.ModelForm):
    class Meta:
        model = Wikistore
        # fields = "__all__"
        fields = ("wikititle", "wikitag", "wikicontent")
        labels = {'wikititle': '', 'wikitag': '', 'wikicontent': ''}
        widgets = {
            'wikititle': TextInput(
                attrs={'class': 'form-control', 'placeholder': '标题', 'style': 'width:86%;margin:0 0 0 7%'}),
            'wikitag': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'tag1,tag2,tag3', 'style': 'width:86%;margin:0 0 0 7%'})
        }


        # exclude=('create_time','update_time','user','update_user','status','wikititle','wikisummary','wikitag')
