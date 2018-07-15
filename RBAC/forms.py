#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 20:12
# @Auther : Wshu


from django import forms
from . import models
from django.forms import ModelForm
from django.forms import widgets


class SigninForm(forms.Form):
    username = forms.CharField(label='账号', max_length=80, widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'用户名'}))
    password = forms.CharField(label='密码',max_length=25,widget=forms.PasswordInput(attrs={'class':'layui-input','placeholder':'密码'}))