#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 14:59
# @Auther : Wshu
import datetime
from . import forms, models
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .service.init_permission import init_permission
from SysconfManage.commFunc.checkpsd import checkpsd
from SysconfManage.views import paging, strtopsd


################################
# 仪表盘
################################
@login_required
def dashboard(request):
    return render(request, 'Dashboard.html')

################################
# 首页
################################
@login_required
def index(request):
    return render(request, 'RBAC/index.html')


################################
# 登录
################################
@csrf_protect
def login(request):
    error = ''
    if request.method == 'POST':
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_get = User.objects.filter(username=username).first()
            if user_get:
                if user_get.profile.lock_time > timezone.now():
                    err = u'账号已锁定,' + str(user_get.profile.lock_time.strftime("%Y-%m-%d %H:M%")) + '后尝试重新登录'
                else:
                    user = authenticate(username=username, password=password)
                    if user:
                        user.profile.error_count = 0
                        user.save()
                        auth.login(request, user)

                        # 调用init_permission 进行权限初始化(补充说明: 因为扩展默认User表,所以初始化权限时需要传入 user.profile)
                        init_permission(request, user.profile)
                        return HttpResponseRedirect('/user/')
                    else:
                        user_get.profile.error_count += 1
                        if user_get.profile.error_count >= 10:
                            user_get.profile.lock_time = timezone.now() + datetime.timedelta(minutes=10)
                        # user_get.save()
                        error = '登录失败,累积错误登录'+ str(user_get.profile.error_count) + '次,10次后账号锁定'
            else:
                error = u"登录失败,仔细检查哦"
        else:
            error = u'请检查输入信息是否正确'
        return render(request, 'RBAC/login.html', {'form':form, 'error':error})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/user/')
        else:
            form = forms.SigninForm()
    return render(request, 'RBAC/login.html', {'form':form})



################################
# 注册
################################
@csrf_protect
def regist(request, argu):
    error = ''
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

################################
# 找回密码
################################
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



################################
# 登出
################################
@login_required
def logout(request):
    auth.logout(request)
    request.session.clear()
    return HttpResponseRedirect('/welcome/')



################################
## 修改密码
################################
@login_required
@csrf_protect
def changepwd(request):
    error = ''
    if request.method == 'POST':
        form = forms.ChangePwdForm()
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            re_new_password = form.cleaned_data['re_new_password']
            username = request.user.username
            if checkpsd(new_password):
                if new_password and new_password == re_new_password:
                    if old_password:
                        user = auth.authenticate(username=username, password=old_password)
                        if user:
                            user.set_password(new_password)
                            user.save()
                            auth.logout(request)
                            error = '修改成功'
                        else:
                            error = '账号信息错误'
                    else:
                        error = '请检查原密码'
                else:
                    error = '两次输入的密码不一致,请自己确认检查'
            else:
                error = '密码必须在6位以上,并且包含数字,字母!'
        else:
            error = '请检查输入'
        return render(request, 'formEdit.html', {'form':form, 'post_url': 'changepwd', 'error':error})
    else:
        form = forms.ChangePwdForm()
        return render(request, 'formEdit.html', {'form':form, 'post_url': 'changepwd'})
################################
# 用户列表
################################
@login_required
@csrf_protect
def userlist(request):
    user = request.user
    error = ''
    if user.is_superuser:
        area = models.Area.objects.filter(parent__isnull=True)
        city = models.Area.objects.filter(parent__isnull=False)
        return render(request, 'RBAC/userList.html', {'area': area, 'city': city})
    else:
        error = '权限错误'
    return render(request, 'error.html', {'error':error})

################################
# 提交注册
################################
@login_required
@csrf_protect
def userregistaction(request):
    user = request.user
    error = ''
    if user.is_superuser():
        regist_id = request.POST.get('request_id')
        action = request.POST.get('action')
        userregist = get_object_or_404(models.UserRequest, id=regist_id)
        if userregist.is_check:
            error = '请勿重复审批'
        else:
            if action == 'access':
                userregist.is_check = True
                userregist.status = '1'
                res = mails.sendregistmail(userregist.email, userregist.urlarg)
                if res:
                    error = '添加成功，已向该员工发送邮件'
                else:
                    error = '添加成功，邮件发送失败，请重试'
                userregist.save()
            else:
                if action == 'deny':
                    userregist.is_check = True
                    userregist.status = '2'
                    userregist.is_use = True
                    userregist.save()
                    error = '已审批'
                else:
                    error = '未指定操作'
    else:
        error = '权限错误'
    return JsonResponse({'error': error})

################################
# 注册用户列表
################################
@login_required
def userregistlist(request):
    user = request.user
    error = ''
    if user.is_superuser:
        area = models.Area.objects.filter(parent__isnull=True)
        return render(request, 'RBAC/userregistlist.html', {'area': area})
    else:
        error = '权限错误'
    return render(request, 'error.html', {'error': error})


################################
# 添加用户
################################
@login_required
@csrf_protect
def user_add(request):
    user = request.user
    error = ''
    if user.is_superuser:
        if request.method == 'POST':
            form = forms.RegistForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user_get = User.objects.filter(username=email)
                if user_get:
                    error = '用户已存在'
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
                            request_type=request_type,
                            is_check=True,
                            status='1',
                            action_user=user
                        )
                        res = mails.sendregistmail(email, urlarg)
                        if res:
                            error = '添加成功，已向该员工发送邮件'
                        else:
                            error = '添加成功，邮件发送失败，请重试'
            else:
                error = '请检查输入'
        else:
            form = forms.RegistForm()
    else:
        error = '请检查权限是否正确'
    return render(request, 'formEdit.html', {'form': form, 'error': error})

################################
## 用户资料
################################

@login_required
def userinfo(request):
    return render(request, 'RBAC/userInfo.html')

################################
## 修改资料
################################
@login_required
@csrf_protect
def changeuserinfo(request):
    user = request.user
    error = ''
    if request.method == 'POST':
        form = forms.UserInfoForm(instance=user.profile)
        if form.is_valid():
            if 'parent_email' in form.changed_data:
                parent_email = form.cleaned_data['parent_email']
                parent_user = User.objects.filter(email=parent_email).first()
                if parent_user:
                    user.profile.parent = parent_user
                    user.save()
            form.save()
            error = '修改成功'
        else:

            error = '修改失败'
        return render(request, 'formEdit.html', {'form':form, 'post_url': 'changeuserinfo', 'error':error})
    else:
        form = forms.UserInfoForm(instance=user.profile)
        return render(request, 'formEdit.html', {'form':form, 'post_url': 'changeuserinfo'})
