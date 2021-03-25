import math
import random
import numpy as np

class CONFIG:
    n_us = 4999
    n_s1 =1
    n_s2 = 0
    n_t = 0
    us_to_s1 = 0.00000371
    s1_to_s2 = 0.00005
    s1_to_t = 0.00009
    s2_to_t = 0.000003
    C = 0.7
    iters = [3000,6999,9856,13331,16989,19536,23698,26985,29631,33654.36985,39632.43756,46956,49632,53698,56321,59632,63214,66987,69632,75621,83698,89654,96632,99965]
    N = 40
    out_path = 'G:\\result.txt'



params = {
    "us_to_s1":1-math.exp(-CONFIG.us_to_s1 * CONFIG.C),
    "s1_to_s2":1-math.exp(-CONFIG.s1_to_s2),
    "s1_to_t":1-math.exp(-CONFIG.s1_to_t),
    "s2_to_t":1-math.exp(-CONFIG.s2_to_t)
    }


def changeCondition(data, params):
    _len = len(data)
    data_copy = data
    for i in range(0, _len):
        if data[i] == 'US':
            for j in range(0, _len):
                if i == j:
                    continue
                if data_copy[j] == 'S1' or data_copy[j] == 'S2':
                    rd = random.random()
                    if rd < params['us_to_s1']:
                        data[i] = 'S1'
                        continue
        elif data[i] == 'S1':
            rd = random.random()
            if rd < params['s1_to_s2']:
                data[i] = 'S2'
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
    data = ['US'] * CONFIG.n_us + ['S1'] * CONFIG.n_s1 + ['S2'] * CONFIG.n_s2 + ['T'] * CONFIG.n_t
    result = []
    for n in range(CONFIG.N):
        for i in range(it):
            data = changeCondition(data, params)
        result.append(cal_condition(data))
    result = np.array(result).mean(axis=0)
    rs.append(result)

out = ""
for item in rs:
    item = list(map(str, item))
    out += ",".join(item)
    out += "\n"

with open(CONFIG.out_path, 'w') as ipt:
    ipt.write(out)