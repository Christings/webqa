# -*- coding: utf-8 -*-
# __author__ = "gongyanli"
from __future__ import unicode_literals, print_function, division
from django import forms
from .models import Wikistore


class EditorTestForm(forms.ModelForm):
    class Meta:
        model = Wikistore
        # fields = "__all__"
        # labels=None
        fields = ("wikititle","wikicontent","wikitag")
        labels = {'wikicontent': ''}



        # exclude=('create_time','update_time','user','update_user','status','wikititle','wikisummary','wikitag')
