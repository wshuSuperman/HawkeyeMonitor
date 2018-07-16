#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/16 14:21
# @Auther : Wshu
import hashlib
from django.contrib.auth.hashers import make_password

def strtopsd(string):
    hash_res = hashlib.md5()
    hash_res.update(make_password(string).encode('utf-8'))
    urlarg = hash_res.hexdigest()
    return urlarg
