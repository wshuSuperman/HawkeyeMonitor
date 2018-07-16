#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 14:59
# @Auther : Wshu
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from SysconfManage.views import strtopsd
from SysconfManage.SmallFun import checkpsd, mails
import django.utils.timezone as timezone
from django.contrib import auth
from . import forms, models
import datetime, hashlib


### 仪表盘
# @login_required
def dashboard(request):
    return render(request, 'Dashboard.html')


### 首页
def index(request):
    return render(request, 'RBAC/index.html')


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


### 用户注册
@csrf_protect
def regist(request, argu):
    error = ""
    if argu == 'regist':
        if request.method == "POST":
            form = forms.RegistForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user_get = User.objects.filter(username=email)
                if user_get:
                    error = "用户名已存在"
                else:
                    userregist_get = models.UserRequest.objects.filter(email=email)
                    if userregist_get.count() > 2:
                        error = '用户已多次添加'
                    else:
                        area = form.cleaned_data['area']
                        request_type = form.cleaned_data['request_type']
                        urlarg = strtopsd(email)
                        models.UserRequest.objects.get_or_create(
                            email=email,
                            urlarg=urlarg,
                            area=area,
                            request_type=request_type
                        )
                        # res = mails.sendregistmail(email, urlarg)
                        error = '申请成功，审批通过后会向您发送邮件'
            else:
                error = '请检查输入'
        else:
            form = forms.RegistForm()
        return render(request, 'RBAC/registrequest.html', {'form': form, 'error': error})
    else:
        resetpsd = get_object_or_404(models.UserResetpsd, urlarg=argu)
        if resetpsd:
            email_get = resetpsd.email
            if request.method == 'POST':
                form = forms.ResetpsdForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    repassword = form.cleaned_data['repassword']
                    if checkpsd(password):
                        if password == repassword:
                            if email_get == email:
                                user = get_object_or_404(User, email=email)
                                if user:
                                    user.set_password(password)
                                    user.save()
                                    resetpsd.delete()
                                    return HttpResponseRedirect('/welcome/')
                                else:
                                    error = '用户信息有误'
                            else:
                                error = '用户邮箱不匹配'
                        else:
                            error = '两次密码不一致'
                    else:
                        error = '密码必须6位以上且包含字母、数字'
                else:
                    error = '请检查输入'
            else:
                form = forms.ResetpsdForm()
            return render(request, 'RBAC/')

### zhuce
@csrf_protect
def resetpasswd(request, argu='resetpsd'):
    error = ''
    if argu == 'resetpsd':
        if request.method == 'POST':
            form = forms.ResetpsdRequestForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = get_object_or_404(User, email=email)
                if user:
                    hash_res = hashlib.md5()
                    hash_res.update(make_password(email).encode('utf-8'))
                    urlarg = hash_res.hexdigest()
                    models.UserResetpsd.objects.get_or_create(
                        email=email,
                        urlarg=urlarg
                    )
                    res = mails.sendregistmail(email, urlarg)
                    if res:
                        error = '申请已发送，请检查邮件通知，请注意检查邮箱'
                    else:
                        error = '重置邮件发送失败，请重试'
                else:
                    error = '重置邮件发送失败，请重试'
            else:
                error = '请检查输入信息'
        else:
            form = forms.ResetpsdRequestForm()
        return render(request, 'RBAC/registrequest.html', {'form': form, 'error': error})
    else:
        resetpsd = get_object_or_404(models.UserResetpsd, urlarg=argu)
        if resetpsd:
            email_get = resetpsd.email
            if request.method == 'POST':
                form = forms.ResetpsdForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    repassword = form.cleaned_data['repassword']
                    if checkpsd(password):
                        if password == repassword:
                            if email_get == email:
                                user = get_object_or_404(User, email=email)
                                if user:
                                    user.set_password(password)
                                    user.save()
                                    resetpsd.delete()
                                    return HttpResponseRedirect('/view/')

                                else:
                                    error = '用户信息有误'
                            else:
                                error = '用户邮箱不匹配'
                        else:
                            error = '两次密码不一致'
                    else:
                        error = '密码必须6位以上且包含字母、数字'
                else:
                    error = '请检查输入'
            else:
                form = forms.ResetpsdForm()
            return render(request, 'RBAC/resetpsd.html', {'form': form, 'error': error, 'title': '重置'})



### 退出
@login_required
def logout(request):
    auth.logout(request)
    request.session.clear()
    return HttpResponseRedirect('/welcome/')



