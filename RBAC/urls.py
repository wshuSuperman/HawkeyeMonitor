#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 18:13
# @Auther : Wshu

from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    ###welcome###
    path('welcome/', views.login, name="login"),
    path('welcome/regist/<str:argu>/', views.regist, name="regist"),
    path('welcome/resetpsd/<str:argu>/', views.resetpasswd, name="resetpsds"),
    ###user###
    path('user/', views.dashboard, name="dashboard"),
    path('user/index', views.index, name="index"),
    path('user/changepwd', views.changepwd, name="changepwd"),
    path('user/info/', views.userinfo, name='userinfo'),
    path('user/changeinfo', views.changeuserinfo, name='changeuserinfo'),
    path('user/logout', views.logout, name="logout"),
    ###manage###
    path('manage/user/', views.userlist, name="userview"),
    path('manage/user/add/', views.user_add, name="useradd"),

    path('manage/userrequest/', views.userregistlist, name="userregistview"),
    path('manage/userrequest/action/', views.userregistaction, name="userregistaction"),
]