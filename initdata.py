#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/16 12:36
# @Auther : Wshu


import django, os

def initment():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC import models
    menu_list = [
                {'title': '资产管理', 'icon': "&#xe653;"},
                {'title': '漏洞管理', 'icon': "&#xe663;"},
                {'title': '任务管理', 'icon': "&#xe628;"},
                {'title': '报表管理', 'icon': "&#xe629;"},
                {'title': '系统配置', 'icon': "&#xe770;"},
    ]

    for item in menu_list:
        models.Menu.objects.get_or_create(
            title=item['title'],
            icon=item['icon']
        )
    submain_list = [
        {'title': '资产列表', 'icon': "&#xe60a;", 'parent_title': '资产管理'},

        {'title': '漏洞列表', 'icon': "&#xe756;", 'parent_title': '漏洞管理'},

        {'title': '漏洞库', 'icon': "&#xe656;", 'parent_title': '漏洞管理'},

        {'title': '任务列表', 'icon': "&#xe60a;", 'parent_title': '任务管理'},

        {'title': '基础报表', 'icon': "&#xe629;", 'parent_title': '报表中心'},

        {'title': '用户列表', 'icon': "&#xe60a;", 'parent_title': '用户管理'},
    ]

    for item in submain_list:
        models.Menu.objects.get_or_create(
            title=item['title'],
            icon=item['icon'],
            parent=models.Menu.objects.filter(title=item['parent_title']).first(),
        )


    permission_list = [
        {'title': '资产列表', 'url': '/asset/user/', 'is_menu': True, 'menu_title': '资产列表'},

        {'title': '漏洞操作', 'url': '/vuln/manage/', 'is_menu': False},
        {'title': '漏洞列表', 'url': '/vuln/user/', 'is_menu': True, 'menu_title': '漏洞列表'},
        {'title': '漏洞库', 'url': '/vuln/cnvd/', 'is_menu': True, 'menu_title': '漏洞库'},

        {'title': '任务列表', 'url': '/task/user/', 'is_menu': True, 'menu_title': '任务列表'},
        {'title': '扫描同步', 'url': '/task/manage/', 'is_menu': False},

        {'title': '基础报表', 'url': '/chart/', 'is_menu': True, 'menu_title': '基础报表'},

        {'title': '用户列表', 'url': '/manage/user/', 'is_menu': True, 'menu_title': '用户列表'},

    ]
    for item in permission_list:
        permission_tup = models.Permission.objects.get_or_create(
            title=item['title'],
            url=item['url']
        )
        permission = permission_tup[0]
        if item['is_menu']:
            permission.menu = models.Menu.objects.filter(title=item['menu_title']).first()
            permission.save()

# 初始化区域
def initarea():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC.models import Area
    area_list =[
        {'name':'华北'},
        {'name':'华南'},
        {'name':'华东'},
        {'name':'华中'},
        ]
    for item in area_list:
        Area.objects.get_or_create(name=item['name'])
    print('initrole ok')


def initrole():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC.models import Role, Permission
    permissions_list = [
        {'title': '安全管理员', 'permissions': '资产列表'},
        {'title': '安全管理员', 'permissions': '漏洞操作'},
        {'title': '安全管理员', 'permissions': '漏洞列表'},
        {'title': '安全管理员', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '安全管理员', 'permissions': '扫描同步'},
        {'title': '安全管理员', 'permissions': '基础报表'},
        {'title': '安全管理员', 'permissions': '用户列表'},

        {'title': '运维管理员', 'permissions': '资产列表'},
        {'title': '运维管理员', 'permissions': '漏洞列表'},
        {'title': '运维管理员', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '运维管理员', 'permissions': '基础报表'},

        {'title': '网络管理员', 'permissions': '资产列表'},
        {'title': '网络管理员', 'permissions': '漏洞列表'},
        {'title': '网络管理员', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '网络管理员', 'permissions': '基础报表'},

        {'title': '业务负责人', 'permissions': '资产列表'},
        {'title': '业务负责人', 'permissions': '漏洞列表'},
        {'title': '业务负责人', 'permissions': '漏洞库'},
        {'title': '安全管理员', 'permissions': '任务列表'},
        {'title': '业务负责人', 'permissions': '基础报表'},
    ]
    for item in permissions_list:
        role_list = Role.objects.get_or_create(title=item['title'])
        role_list[0].permissions.add(Permission.objects.filter(title=item['permissions']).first())
        role_list[0].save()

    print('initrole ok')


def initsuperuser():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HawkEyeProbe.settings')
    django.setup()
    from RBAC.models import Role
    from django.contrib.auth.models import User
    user_manage_list = User.objects.filter(is_superuser=True)
    role = Role.objects.filter(title='安全管理员').first()
    for user in user_manage_list:
        user.profile.roles.add(role)
        user.save()
    print('initsuperuser ok')


if __name__ == '__main__':
    initment()
    initarea()
    initrole()
    initsuperuser()