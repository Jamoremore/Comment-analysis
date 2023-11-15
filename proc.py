# 生成process_file函数。输入产品名、品牌名、excel，输出新的excel文件并保存
import streamlit as st
import os
import shutil
import datetime
from io import BytesIO

from paddlenlp import Taskflow
from tqdm import *
# 引入pandas库
import pandas as pd

from typing import List
from rich import print



def get_pl(data:list,
           prod_label:list,
           brand_label:list,
           my_ie
           ):
    # 输入评论、需要踩中的关键词，返回筛选后的评论
    # 输出评论
    ans = []

    for i in tqdm(data):
        temp = my_ie(i)
        if temp == [{}]:
            # 如果没有提到产品或者品牌，保存
            ans.append(i)
        else:
            check = False
            # 如果有目标产品名，保存
            for j in prod_label:
                if j in i:
                    check = True
                    break
            # 如果没提到产品名，提到了目标品牌名，保存
            if '产品' not in temp[0]:
                for j in brand_label:
                    if j in i:
                        check = True
                        break
            if check:
                ans.append(i)
    return ans


def remove_non_gb2312(text):
    res = []
    for char in text:
        try:
            char.encode('GB2312')
            res.append(char)
        except UnicodeEncodeError:
            pass
    return ''.join(res)


def get_opt(text):
    # 删除错误文件
    model_path = "./model/static"
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    schema = ['主推产品']
    my_ie = Taskflow("information_extraction", schema=schema, task_path='./model')
    opt = "########原文########\n"+text+"\n\n########输出结果########\n"

    cnt = 1

    # my_ie = get_my_ie()
    # 删除特殊符号
    text = remove_non_gb2312(text)
    temp = my_ie(text)
    if '主推产品' in temp[0]:
        for j in temp[0]['主推产品']:
            # 删除低概率的判定结果
            if j['probability'] >= 0.5:
                opt = opt + "id:" + str(cnt) + "\n    text:" + j['text'] + "\n    prob:" + str(j['probability']) + '\n'
                cnt = cnt + 1
    print(opt)
    with open('data/logs.txt', 'a', encoding='utf-8') as ins_test_file:
        current_time = datetime.datetime.now()
        ins_test_file.write(current_time.strftime("%Y/%m/%d %H:%M:%S\n") + opt + '\n\n')

    return opt


def get_label(r1, r2, my_ie):
    if pd.isnull(r1):
        r1 = ""
    if pd.isnull(r2):
        r2 = ""
    text = remove_non_gb2312(r1+'\n'+r2)
    temp = my_ie(text)
    opt = ""
    cnt = 1
    if '主推产品' in temp[0]:
        for j in temp[0]['主推产品']:
            # 删除低概率的判定结果
            if j['probability'] >= 0.5 and len(j['text']) < 50:
                opt = opt + "text" + str(cnt) + ":" + j['text'] + ";\n"
                cnt = cnt + 1
    return opt


def process_file(product, brand, df):
    # # 删除错误文件
    # model_path = "./model/static"
    # if os.path.exists(model_path):
    #     shutil.rmtree(model_path)
    schema = ['品牌', '产品']

    # 设定抽取目标和定制化模型权重路径
    my_ie = Taskflow("information_extraction", schema=schema, task_path='./checkpoint/paddlenlp_120')

    col = df.iloc[:, 0].tolist()  # 获取第一列数据并转化为列表，

    prod_label = product.split(';')[:-1]
    brand_label = brand.split(';')[:-1]

    # 筛选评论，
    data1 = get_pl(col, prod_label, brand_label, my_ie)

    # .read() 会返回 bytes, 所以我们要把它转换成字符串
    # 逐行读取第一列和第二列的内容，计算f(col1, col2)，并将结果保存到第三列
    df[2] = df.apply(lambda row: get_label(row[0], row[1], my_ie), axis=1)

    # 保存结果到本地
    current_time = datetime.datetime.now()
    df.to_excel('data/' + current_time.strftime("%Y_%m_%d %H_%M_%S") + '.xlsx', index=False)
    # 绘制结果
    st.write(df)

    # 将DataFrame转化为Excel并存储在BytesIO对象中
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    # 重置指针位置
    excel_file.seek(0)

    # 使用st.download_button创建一个可以下载Excel文件的按钮
    st.download_button(
        label="下载Excel文件",
        data=excel_file,
        file_name='output.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    return ""