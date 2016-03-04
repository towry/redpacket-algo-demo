#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import sys, path 

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import math
import random
from random import uniform
from random import expovariate as exp
from scripts.filelog import Filelog

"""
测试红包算法
"""

class Pack(object):
    def __init__(self, money):
        self._remain_money = money

    @property
    def remain_money(self):
        return self._remain_money
    @remain_money.setter
    def remain_money(self, value):
        self._remain_money = value


def get_money(pack, max, min):
    if max <= min:
        raise ValueError("max < min")

    hdelta = max - min

    if pack.remain_money <= min:
        # send or not send
        money = pack.remain_money
        money = math.floor(money * 100) / 100
        pack.remain_money = 0
        return money

    random.seed()
    percent = random.random()
    delta_money = hdelta * percent
    money = math.floor((min + delta_money) * 100) / 100

    if money > pack.remain_money:
        money = pack.remain_money
        money = math.floor(money * 100) / 100
        pack.remain_money = 0
        return money

    pack.remain_money -= money
    return money

"""
max = 100
min = 1
average = (100 + 1) / 2 = 50
left_max = average
right_min = average
left_money = total_money + (total_money * random / 2)
right_money = total_money - left_money
"""
def get_exp_money(pack, max, min):
    if max <= min:
        raise ValueError("max < min")

    if pack.remain_money <= min:
        # 剩余的钱少于min，发还是不发呢?
        money = pack.remain_money
        money = math.floor(money * 100) / 100
        pack.remain_money = 0
        return money

    average = (max + min) / 2
    hdelta = max - min
    lambd = 1.0 / average
    money = exp(lambd)
    if money < min:
        money = min + hdelta * ((min - money) / min)
    if money > max:
        money = max - hdelta * ((money - max) / money)

    # TODO: 这里要特意处理，剩余的钱和min的钱
    if money > pack.remain_money:
        money = pack.remain_money
        money = math.floor(money * 100) / 100
        pack.remain_money = 0
        return money

    money = math.floor(money * 100) / 100
    pack.remain_money -= money
    return money


def _average_round(total_money, max, min):
    if max < min:
        raise ValueError("max < min")

    pack = Pack(total_money)
    res = []
    while pack.remain_money > 0:
        money = get_money(pack, max, min)
        res.append(money)

    return res

def _average_rounds(flog, total_money, max, min, json_only=False):
    total_rounds = 100
    total_list = []
    while total_rounds > 0:
        total_rounds -= 1

        # # half_money = total_money / 2
        # max = 100
        # min = 2

        # half_less = _average_round(half_money, middle, min)
        # half_more = _average_round(half_money, max, middle)
        # half_less.extend(half_more)
        # res = half_less
        # 
        res = _average_round(total_money, max, min)

        if json_only:
            dic = dict()
            dic['data'] = res
            dic['max'] = max 
            dic['min'] = min 
            dic['total_money'] = total_money
            total_list.append(dic)
        else:
            dic = res
            flog.round(dic, json_only)
        
        # res.sort()
        # print "average amount: {}".format(len(res))
        # print "result: "
        # print res 
        # print ""
    flog.round(total_list, json_only)
    flog.done()


def _exp_round(total_money, max, min):
    pack = Pack(total_money)

    res = []
    while pack.remain_money > 0:
        money = get_exp_money(pack, max, min)
        res.append(money)
    return res


def _exp_rounds(flog, total_money, max, min, json_only=False):
    total_rounds = 100
    total_list = []
    while total_rounds > 0:
        total_rounds -= 1
        
        res = _exp_round(total_money, max, min)

        if json_only:
            dic = dict()
            dic['data'] = res 
            dic['max'] = max 
            dic['min'] = min 
            dic['total_money'] = total_money
            total_list.append(dic)
        else:
            dic = res 
            flog.round(dic, json_only)
    flog.round(total_list, json_only)
    flog.done()
        

def is_int(n):
    try:
        int(n)
        return True
    except Exception as e:
        return False


if __name__ == '__main__':

    typo = raw_input("Please select the type: [a, e]\na: average\ne:expo\n")
    if typo != 'a' and typo != 'e':
        exit("wrong choice :" + typo)

    money = raw_input("Please input the total money:\n")
    if not is_int(money):
        exit("wrong argument")
    _max = raw_input("Please input the max money:\n")
    if not is_int(_max):
        exit("wrong argument")
    _min = raw_input("Please input the min money:\n")
    if not is_int(_min):
        exit("wrong argument")

    root = path.join(path.dirname(path.abspath(__file__)), '_results')

    if typo == 'a':
        prefix = 'average'
    else:
        prefix = 'exp'

    money = int(money)
    _max = int(_max)
    _min = int(_min)

    flog = Filelog(root, prefix)

    if typo == 'a':
        _average_rounds(flog, money, _max, _min, True)
    else:
        _exp_rounds(flog, money, _max, _min, True)
