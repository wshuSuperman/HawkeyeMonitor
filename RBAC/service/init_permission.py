#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wshu'
"""
    ***********************************
    *  @filename : init_permission.py
    *  @Author : wshu
    *  @CodeDate : 19-7-2 下午3:46
    *  @Software : PyCharm
    ***********************************
"""
from django.conf import settings

from ..models import Menu

def init_permission(request, user_obj):
    """
    前端页面使用,把当前登录用户的权限放在session中,request参数指前端传入的当前login请求的request
    :param request: 当前请求
    :param user_obj: 当前登录用户
    :return: None
    """
    # 拿到当前用户的权限信息
    permission_item_list = user_obj.roles.values('permissions__url',
                                                 'permissions__title',      # 用户列表
                                                 'permissions__menu_id'     # 当前权限所在组的id
                                                 ).distinct()
    permission_url_list = []
    # 用户权限url列表, --> 用于中间件验证用户权限
    permission_menu_list = []
    # 用户权限url所属菜单列表[{'title':'xxx', "url":xxx, "menu_id":'xxx'}, {},]
    for item in permission_item_list:
        permission_url_list.append(item['permissions__url'])
        if item['permissions__menu_id']:
            temp = {'title':item['permissions__title'],
                    'url':item['permissions__url'],
                    'menu_id':item['permissions__menu_id']}
            permission_menu_list.append(temp)

    menu_list = list(Menu.objects.values('id', 'title', 'icon', 'parent_id'))
    # 注: session在存储时,会先对数据进行序列化,因此对于Queryset对象写入session,加list()转为可序列化对象

    # 保存用户权限url列表
    request.session[settings.SESSION_PERMISSION_URL_KEY] = permission_url_list

    # 保存 权限菜单 和 所有菜单: 用户登录后作菜单展示用
    request.session[settings.SESSION_MENU_KEY] = {
        settings.ALL_MENU_KEY: menu_list,
        settings.PERMISSION_MENU_KEY: permission_menu_list,
    }