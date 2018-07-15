#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 14:59
# @Auther : Wshu
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
import django.utils.timezone as timezone
from django.contrib import auth
from . import forms, models
import datetime


### 仪表盘
def dashboard(request):
    return render(request, 'Dashboard.html')


### 基页
def master(request):
    return render(request, 'index.html')


### 登录
def login(request):
    error = ''
    if request.method == "POST":
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_get = User.objects.filter(username=username).first()
            if user_get:
                if user_get.profile.lock_time > timezone.now():
                    error = u'账号已锁定,' + str(user_get.profile.lock_time.strftime("%Y-%m-%d %H:%M")) + '后可尝试'
                else:
                    user = auth.authenticate(username=username, password=password)
                    if user:
                        user.profile.error_count = 0
                        user.save()
                        auth.login(request, user)
                        return HttpResponseRedirect('/user/')
                    else:
                        user_get.profile.error_cout += 1
                        if user_get.profile.error_cout >= 5:
                            user_get.profile.error_cout = 0
                            user_get.profile.lock_time = timezone.now() + datetime.timedelta(minutes=10)
                        user_get.save()
                        error = '登陆失败,已错误登录'+str(user_get.profile.error_count) +'次,5次后账号锁定',
            else:
                error = error = '请检查用户信息'
        else:
            error = u'请检查输入'
        return render(request,'RBAC/login.html',{'form':form,'error':error})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/user/')
        else:
            form = forms.SigninForm()
    return render(request, 'RBAC/login.html', {'form': form})


### 退出
def logout(request):
    pass



