# 完整实现评论筛选和排序
# 首先采用paddlenlp对竞品评论进行筛除，然后通过评论筛除模型进行评论价值评分

import subprocess
from save_load import save
import pandas as pd
import re
from pandas import isnull

# from inference import inference
# from get_pl import get_pl

import csv
from rich import print


def get_dim():
    t_data = open('./data/dim-v2.txt', 'r', encoding='utf-8').readlines()
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


def myfill(ls, maxlen):
    # 在ls的末尾填充空字符
    ls += [''] * (maxlen - len(ls))
    return ls


def cal_act_len(text:str):
    text = re.sub('@\S*\s*', '', text)
    text = re.sub('\[[^\[\]\n]*\]', '', text)
    punctuations = ",，.。:：？? ;；!！~、"
    # 创建一个映射表，将所有标点符号映射到None
    trans_table = str.maketrans('', '', punctuations)
    # 使用映射表来删除标点符号
    text = text.translate(trans_table)
    return len(text)


def comment_sort(product, brand, df):
    # ##################################################################
    # 数据预处理
    # 删除重复数据，根据句子长度，删除长度低于2和高于80的句子。
    print("preprocessing data...")
    text = df.iloc[:, 0].tolist()  # 获取第一列数据并转化为列表，
    maxlen = len(text)
    text1 = []
    for i in text[1:]:
        if isnull(i):
            continue
        i = str(i)
        if i not in text1 and 2 < len(i) < 80:
            text1.append(i)
    ac_len = []
    for i in text1:
        ac_len.append(cal_act_len(i))
    text = []
    # 根据长度做排序
    for item, score in sorted(zip(text1, ac_len), key=lambda x: x[1], reverse=False):
        if score > 2:
            text.append(item)

    # ##################################################################
    # 关键信息提取与关键词筛选
    print("key word sorting...")

    # 创建要写入的数据
    save({"data": [text, brand, product], "id": ["text", "brand", "product"]})

    subprocess.call(["python", "get_pl.py"])

    # ##################################################################
    # 剔除模型
    # 0表示有效
    print("model loading...")
    subprocess.call(["python", "inference.py"])

    # ##################################################################
    # 结果输出
    # 读取CSV文件
    df1 = pd.read_csv('./temp/temp.csv')

    # 提取'data'列
    data = df1['data'].dropna().tolist()
    score = df1['score'].dropna().tolist()

    opt_data = []

    score1 = []
    for item, score in sorted(zip(data, score), key=lambda x: x[1], reverse=True):
        opt_data.append(item)
        score1.append(score)

    # # 调整Dataframe的大小
    # df = df.iloc[:len(opt_data)+1, :]

    df["data"] = myfill(opt_data, maxlen)
    df["score"] = myfill(score1, maxlen)

    # 获取维度
    dims, labels = get_dim()

    for i in data:
        check = True
        for j in dims:
            for k in j["keys"]:
                temp = re.sub('@\S*\s*', '', i)
                temp = re.sub('\[[^\[\]\n]*\]', '', temp)
                if k in temp:
                    labels[j["label"]].append(i)
                    check = False
        if check:
            labels["其他"].append(i)

    for i in dims:
        df[i["label"]] = myfill(labels[i["label"]], maxlen)

    return df