# 读all_data.txt的内容，然后输出为paddlenlp所用的训练数据
import random
import re
import pandas as pd
import math
from tqdm import *
import time


def get_dim():
    t_data = open('data/dim-v2.txt', 'r', encoding='utf-8').readlines()
    dim = []
    label={}
    for i in range(len(t_data)):
        t0 = {}
        t1 = t_data[i].split('\t')
        t0["label"] = t1[0]
        t0["keys"] = t1[1].split('\n')[0].split(',')
        t0['label_id'] = i
        label[t1[0]]=[]
        dim.append(t0)
    label["其他"] = []
    return dim, label


def dp_dps(df, data):
    # 获取维度
    dims, labels = get_dim()

    for i in data:
        check = True
        for j in dims:
            for k in j["keys"]:
                if k in i:
                    labels[j["label"]].append(i)
                    check = False
        if check:
            labels["其他"].append(i)


