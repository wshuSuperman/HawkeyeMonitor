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
    path('user/logout', views.logout, name="logout"),
    path('user/chang', views.logout, name="logout"),
]