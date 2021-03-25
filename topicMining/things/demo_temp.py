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
    # 定义其他社区
    n_other = n_us + n_s1 + n_s2 + n_t
    us_to_s1 = 0.00000371
    s1_to_s2 = 0.00005
    s1_to_t = 0.00009
    s2_to_t = 0.000003
    C = 0.8
    Q = 0.8
    R1 = 0.5
    R2 = 0.5
    iters = [3999, 7999, 11999, 15999, 19999, 23999, 27999, 31999, 35999, 39999, 43999, 47999, 51999, 55999, 59999,
             63999, 67999, 71999, 75999, 79999, 83999, 87999, 91999, 95999, 99999]
    N = 10
    out_path = 'G:\\result.txt'


s1_to_s2 = 1 - math.exp(-CONFIG.s1_to_s2)
s1_to_t = 1 - math.exp(-CONFIG.s1_to_t)
s2_to_t = 1 - math.exp(-CONFIG.s2_to_t)

params = {
    "s1_to_s2": s1_to_s2,
    "s1_to_t": s1_to_t,
    "s2_to_t": s2_to_t
}


def changeCondition(data, params):
    _len = len(data)
    data_copy = copy.deepcopy(np.array(data))
    n_s = (data_copy == 'S1').sum() + (data_copy == 'S2').sum()
    us_to_s1 = 1 - math.pow(1 - params['us_to_s1'], n_s)
    for i in range(0, _len):
        if data[i] == 'US':
            rd = random.random()
            if rd < us_to_s1:
                data[i] = 'S1'
                continue
        elif data[i] == 'S1':
            rd = random.random()
            if rd < params['s1_to_s2']:
                data[i] = 'S2'
            if rd > 1 - params['s1_to_t']:
                data[i] = 'T'
        elif data[i] == 'S2':
            rd = random.random()
            if rd < params['s2_to_t']:
                data[i] = 'T'
        else:
            continue
    return data


# 传入多个社区的数据
def changeCondition2(data_total_combine, data_total, params):
    # 依次遍历5个社区的节点，逻辑同changeCondition，每一步都要计算当前社区和其他社区中S1和S2的节点数，据此计算转化概率
    total_len = len(data_total_combine)
    # 测试深浅拷贝区别
    # data_total_copy = copy.deepcopy()
    X, Z, Xi, Zi, Xj, Zj = calculateXZ(data_total, 1)
    # print(X, Z, Xi, Zi, Xj, Zj)
    # 根据当前X和Z数量，计算单个转化概率
    us_to_s1_single = calculateUS2S1(X, Z, Xi, Zi, Xj, Zj)
    # print("us_to_s1_single = ", us_to_s1_single)
    n_s = (np.array(data_total_combine) == 'S1').sum() + (np.array(data_total_combine) == 'S2').sum()
    # print("n_s = ", n_s)
    us_to_s1 = (1 - math.pow(1 - us_to_s1_single, n_s))
    for i in range(0, total_len):
        # print("i = ", i)
        if data_total_combine[i] == 'US':
            rd = random.random()
            if rd < us_to_s1:
                data_total_combine[i] = 'S1'
                continue
        elif data_total_combine[i] == 'S1':
            rd = random.random()
            if rd < params['s1_to_s2']:
                data[i] = 'S2'
            if rd > 1 - params['s1_to_t']:
                data[i] = 'T'
        elif data_total_combine[i] == 'S2':
            rd = random.random()
            if rd < params['s2_to_t']:
                data[i] = 'T'
        else:
            continue

    return data_total_combine


# 根据当前X和Z数量，计算转化概率
def calculateUS2S1(X, Z, Xi, Zi, Xj, Zj):
    part_1 = math.pow(1 - (1 - CONFIG.R1) * (1 - CONFIG.R2), X + Z)
    part_2 = CONFIG.C * (Xi + Zi) + (1 - CONFIG.Q) * (Xj + Zj)
    # print("part_1 = ", part_1)
    # print("part_2 = ", part_2)
    # print("-CONFIG.us_to_s1 * part_1 * part_2 = ", -CONFIG.us_to_s1 * part_1 * part_2)

    return 1 - math.exp(-CONFIG.us_to_s1 * part_1 * part_2)


# 传入data和当前社区号，分别输出X Z Xi Zi Xj Zj
def calculateXZ(data_total, current_K):
    X = 0
    Z = 0
    Xi = 0
    Zi = 0
    Xj = 0
    Zj = 0
    n_s = []
    for data in data_total:
        data = np.array(data)
        n_s1 = (data == 'S1').sum()
        n_s2 = (data == 'S2').sum()
        X += n_s1
        Z += n_s2
        n_s.append((n_s1, n_s2))

    # 处理n_s，得到X和Z
    length = len(n_s)
    for i in range(length):
        n_s1 = n_s[i][0]
        n_s2 = n_s[i][1]
        if current_K != i:
            Xj += n_s1
            Zj += n_s2
        else:
            Xi = n_s1
            Zi = n_s2

    return X, Z, Xi, Zi, Xj, Zj


def cal_condition(data):
    data = np.array(data)
    return [(data == 'US').sum(), (data == 'S1').sum(), (data == 'S2').sum(), (data == 'T').sum()]


rs = []
for it in CONFIG.iters:
    print("---大循环第：{}次".format(it))
    result = []
    for n in range(CONFIG.N):
        data = ['US'] * CONFIG.n_us + ['S1'] * CONFIG.n_s1 + ['S2'] * CONFIG.n_s2 + ['T'] * CONFIG.n_t
        data_2 = ['US'] * CONFIG.n_other
        data_3 = ['US'] * CONFIG.n_other
        data_4 = ['US'] * CONFIG.n_other
        data_5 = ['US'] * CONFIG.n_other
        data_total = [data, data_2, data_3, data_4, data_5]
        # print("data_total = ", data_total)

        # 将data_total合并为一个大列表
        data_total_combine = []
        for data in data_total:
            data_total_combine.extend(data)
        # data_total_combine = list(itertools.chain(*map(eval, data_total)))
        # print("data_total_combine = ", data_total_combine)
        it = int(it)
        now = time.time()
        print("---小循环第：{}次".format(n))
        for im in range(it):
            data = changeCondition2(data_total_combine, data_total, params)
            # data = changeCondition(data, params)
        result.append(cal_condition(data))
        end = time.time()
        print("运行时间：{}秒".format(end - now))

        # S1_sum = (np.array(data_total_combine) == 'S1').sum()
        # S2_sum = (np.array(data_total_combine) == 'S2').sum()
        # print("S1_num = ", S1_sum, ", S2_num = ", S2_sum)

    result = np.array(result).mean(axis=0)
    rs.append(result)

out = ""
for item in rs:
    item = list(map(str, item))
    out += ",".join(item)
    out += "\n"

with open(CONFIG.out_path, 'w') as ipt:
    ipt.write(out)
