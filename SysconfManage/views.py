#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/16 14:21
# @Auther : Wshu
import hashlib
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 该代码用来分页

def paging(deploy_list, limit, offset):

    paginator = Paginator(deploy_list, limit)
    try:
        deploy_list = paginator.page(offset)
    except PageNotAnInteger:
        deploy_list = paginator.page(1)
    except EmptyPage:
        deploy_list = paginator.page(paginator.num_pages)
    return deploy_list


def strtopsd(string):
    hash_res = hashlib.md5()
    hash_res.update(make_password(string).encode('utf-8'))
    urlarg = hash_res.hexdigest()
    return urlarg