import math
import random
import numpy as np
import time
import copy

class CONFIG:
    n_us = 4999
    n_s1 = 1
    n_s2 = 0
    n_t = 0
    us_to_s1 = 0.00000371
    s1_to_s2 = 0.00005
    s1_to_t = 0.00009
    s2_to_t = 0.000003
    C = 0.7
    iters = [3999, 7999, 11999, 15999, 19999, 23999, 27999, 31999, 35999, 39999, 43999, 47999, 51999, 55999, 59999, 63999, 67999, 71999, 75999, 79999, 83999, 87999, 91999, 95999, 99999]
    # iters = [3999, 7999, 11999, 15999, 19999, 23999, 27999, 31999, 35999, 39999, 43999, 47999, 51999, 55999, 59999, 63999, 67999, 71999, 75999, 79999, 83999, 87999, 91999, 95999, 99999]
    N = 10
    out_path = 'G:\\result.txt'


us_to_s1= 1-math.exp(-CONFIG.us_to_s1 * CONFIG.C)
s1_to_s2= 1-math.exp(-CONFIG.s1_to_s2)
s1_to_t= 1-math.exp(-CONFIG.s1_to_t)
s2_to_t= 1-math.exp(-CONFIG.s2_to_t)

params = {
    "us_to_s1":us_to_s1,
    "s1_to_s2":s1_to_s2,
    "s1_to_t":s1_to_t,
    "s2_to_t":s2_to_t
    }

#
# def changeCondition(data, params):
#     _len = len(data)
#     data_copy = data
#     for i in range(0, _len):
#         if data[i] == 'US':
#             for j in range(0, _len):
#                 if i == j:
#                     continue
#                 if data_copy[j] == 'S1' or data_copy[j] == 'S2':
#                     rd = random.random()
#                     if rd < params['us_to_s1']:
#                         data[i] = 'S1'
#                         continue
#         elif data[i] == 'S1':
#             rd = random.random()
#             if rd < params['s1_to_s2']:
#                 data[i] = 'S2'
#             if rd > 1-params['s1_to_t']:
#                 data[i] = 'T'
#         elif data[i] == 'S2':
#             rd = random.random()
#             if rd < params['s2_to_t']:
#                 data[i] = 'T'
#         else:
#             continue
#     return data
#
#

#
# def changeCondition(data, params):
#     _len = len(data)
#     data_copy = copy.deepcopy(np.array(data))
#     n_s = (data_copy == 'S1').sum() + (data_copy == 'S2').sum()
#     for i in range(0, _len):
#         if data[i] == 'US':
#             for j in range(0, n_s):
#                 rd = random.random()
#                 if rd < params['us_to_s1']:
#                     data[i] = 'S1'
#                     continue
#         elif data[i] == 'S1':
#             rd = random.random()
#             if rd < params['s1_to_s2']:
#                 data[i] = 'S2'
#             if rd > 1-params['s1_to_t']:
#                 data[i] = 'T'
#         elif data[i] == 'S2':
#             rd = random.random()
#             if rd < params['s2_to_t']:
#                 data[i] = 'T'
#         else:
#             continue
#     return data



def changeCondition(data, params):
    _len = len(data)
    data_copy = copy.deepcopy(np.array(data))
    n_s = (data_copy == 'S1').sum() + (data_copy == 'S2').sum()
    us_to_s1 = 1-math.pow(1-params['us_to_s1'], n_s)
    # print("us_to_s1 = ", us_to_s1)
    for i in range(0, _len):
        if data[i] == 'US':
            rd = random.random()
            if rd < us_to_s1:
                data[i] = 'S1'
                # print("US → S1")
                continue
        elif data[i] == 'S1':
            rd = random.random()
            if rd < params['s1_to_s2']:
                data[i] = 'S2'
                # print("S1 → S2")
            if rd > 1-params['s1_to_t']:
                data[i] = 'T'
        elif data[i] == 'S2':
            rd = random.random()
            if rd < params['s2_to_t']:
                data[i] = 'T'
        else:
            continue
    return data


def cal_condition(data):
    data = np.array(data)
    return [(data == 'US').sum(), (data == 'S1').sum(), (data == 'S2').sum(), (data == 'T').sum()]



rs = []
for it in CONFIG.iters:
    print("---大循环第：{}次".format(it))
    result = []
    for n in range(CONFIG.N):
        data = ['US'] * CONFIG.n_us + ['S1'] * CONFIG.n_s1 + ['S2'] * CONFIG.n_s2 + ['T'] * CONFIG.n_t
        it = int(it)
        now = time.time()
        print("---小循环第：{}次".format(n))
        for im in range(it):
            data = changeCondition(data, params)
        result.append(cal_condition(data))
        end = time.time()
        print("运行时间：{}秒".format(end - now))
    result = np.array(result).mean(axis=0)
    rs.append(result)

out = ""
for item in rs:
    item = list(map(str, item))
    out += ",".join(item)
    out += "\n"

with open(CONFIG.out_path, 'w') as ipt:
    ipt.write(out)