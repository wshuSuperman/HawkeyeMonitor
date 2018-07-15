#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/15 14:59
# @Auther : Wshu

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index")
]
