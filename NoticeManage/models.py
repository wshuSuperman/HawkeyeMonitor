#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wshu'
"""
    ***********************************
    *  @filename : models.py
    *  @Author : wshu
    *  @CodeDate : 19-9-2 下午3:08
    *  @Software : PyCharm
    ***********************************
"""

from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone

NOTICE_TYPE = [
    ('notice', '任务通知'),
    ('sysinfo', '系统通知'),
]



class Notice(models.Model):
    notice_title = models.CharField('通知标题', max_length=50)
    notice_body = models.TextField('通知内容')
    notice_status = models.BooleanField('阅读状态', default=False)
    notice_url = models.CharField('父链接', max_length=50, null=True)
    notice_type = models.CharField('通知类型', max_length=30, choices=NOTICE_TYPE)
    notice_time = models.DateTimeField('通知日期', default=timezone.now)

    notice_user = models.ForeignKey(User, related_name='notice_for_user', verbose_name=u'所属用户', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "系统通知"

    def __str__(self):
        return self.notice_title