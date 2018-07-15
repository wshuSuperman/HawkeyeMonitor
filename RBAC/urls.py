#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 18:13
# @Auther : Wshu

from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    ###view###
    path('welcome/', views.login, name="login"),
    ###user###
    path('user/', views.dashboard, name="dashboard"),
    path('user/master', views.master, name="master"),
    path('user/logout', views.logout, name="logout"),
]