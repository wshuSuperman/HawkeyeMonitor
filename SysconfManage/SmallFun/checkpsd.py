#!/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time : 2018/7/16 14:33
# @Auther : Wshu

import re
def checkpsd(passwd):
    p = re.match(r'^(?=.*?\d)(?=.*?[a-zA-Z]).{6,}$',passwd)
    if p:
        return True
    else:
        return False



if __name__ == '__main__':
    pass