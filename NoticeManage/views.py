#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wshu'
"""
    ***********************************
    *  @filename : views.py
    *  @Author : wshu
    *  @CodeDate : 19-9-2 下午3:08
    *  @Software : PyCharm
    ***********************************
"""

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from . import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.utils.html import escape

from SysconfManage.views import paging
import json

## 功能: 单条已读
@login_required
def notice_read(request, notice_id):
    user = request.user
    notice = get_object_or_404(models.Notice, notice_user=user, id=notice_id)
    notice.notice_status = True
    notice.save()
    return HttpResponseRedirect(notice.notice_url)


## 功能: 通知消息Tables
@login_required
@csrf_protect
def notice_table_list(request):
    user = request.user
    resdt = {}

    page = request.POST.get('page')
    rows = request.POST.get('limit')
    notice_type = request.POST.get('notice_type')
    if not notice_type:
        notice_type = ''
    notice_status = request.POST.get('notice_status')
    if not notice_status:
        notice_status = ['True', 'False']
    else:
        notice_status = [notice_status]

    notice_list = models.Notice.objects.filter(notice_user=user, notice_status__in=notice_status,
                                               notice_type__icontains=notice_type).order_by('-notice_time')
    notice_total = notice_list.count()
    notice_list = paging(notice_list, rows, page)
    data = []
    for notice in notice_list:
        dt = {}
        dt['id'] = escape(notice.id)
        dt['notice_title'] = escape(notice.notice_title)
        dt['notice_body'] = escape(notice.notice_body)
        if notice.notice_status:
            dt['notice_status'] = escape('已读')
        else:
            dt['notice_status'] = escape('未读')
        dt['notice_time'] = escape(notice.notice_time)
        data.append(dt)

    resdt['code'] = 0
    resdt['msg'] = '用户申请列表'
    resdt['count'] = notice_total
    resdt['data'] = data
    return JsonResponse(resdt)


# 功能: 通知数量统计
@login_required
def notice_count(request):
    user = request.user
    notice_count = user.notice_for_user.filter(notice_status=False).count()
    return JsonResponse({'notice_count': notice_count})


## 功能: 通知视图
@login_required
def notice_view(request):
    user = request.user
    return render(request, 'NoticeManage/noticeList.html')


## 功能: 通知操作
@login_required
@csrf_protect
def notice_action(request):
    user = request.user
    tips = '操作成功'
    notice_id_list = request.POST.get('notice_id_list')
    notice_id_list = json.loads(notice_id_list)
    action = request.POST.get('action')
    for notice_id in notice_id_list:
        notice_get = get_object_or_404(models.Notice, notice_user=user, id=notice_id)
        if action == 'delete':
            notice_get.delete()
        elif action == 'read':
            notice_get.notice_status = True
            notice_get.save()
        elif action == 'unread':
            notice_get.notice_status = False
            notice_get.save()
        else:
            tips = '参数错误'
    return JsonResponse({'error': tips})


## 功能: 全部已读
@login_required
def notice_readall(request):
    user = request.user
    tips = '操作成功'
    action = request.POST.get('action')
    if action == 'readall':
        notice_list = user.notice_for_user.filter(notice_status=False)
        for notice_get in notice_list:
            notice_get.notice_status = True
            notice_get.save()
    else:
        tips = '参数错误'
    return JsonResponse({'error': tips})






## 通知增加
def notice_add(user, data):
    """
    :param user: 用户
    :param data: 为字典类型格式
    {
        'notice_title': 'xxxxxxxxxxxx',
        'notice_url': 'xxxxxxxxxxxx',
        'notice_body': 'xxxxxxxxxxxx',
        'notice_type': 'xxxxxxxxxxxx'
    }
    """
    notice_title = data.get('notice_title')
    notice_body = data.get('notice_body')
    notice_url = data.get('notice_url')
    notice_type = data.get('notice_type')

    notice_body = notice_body

    rsp = models.Notice.objects.get_or_create(
        notice_title = notice_title,
        notice_body = notice_body,
        notice_url = notice_url,
        notice_type = notice_type,
        notice_user= user
    )
    if rsp[1]:
        return False
    else:
        rsp[0].notice_status = False
        rsp[0].save()
        return True