#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 14:59
# @Auther : Wshu

from django.shortcuts import render
from django.http import HttpResponse


### 仪表盘
def dashboard(request):
    return render(request, 'Dashboard.html')


### 基页
def master(request):
    return render(request, 'index.html')


### 登录
def login(request):
    return render(request, 'RBAC/login.html')



### 退出
def logout(request):
    pass



