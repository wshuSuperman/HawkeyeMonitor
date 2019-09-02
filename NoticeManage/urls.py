#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wshu'
"""
    ***********************************
    *  @filename : urls.py
    *  @Author : wshu
    *  @CodeDate : 19-9-2 下午3:08
    *  @Software : PyCharm
    ***********************************
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.notice_view, name='noticeview'),     ## 通知视图
    path('list/', views.notice_table_list, name='noticelist'),      ## 通知列表
    path('count/', views.notice_count, name='noticecount'),     ## 通知总量
    path('action/', views.notice_action, name='noticeaction'),     ## 通知操作
    path('readall/', views.notice_readall, name='noticereadall'),     ## 全部已读
    path('read/<str:notice_id>/', views.notice_read, name='noticeread'),     ## 单条已读
]
