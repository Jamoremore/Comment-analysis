from paddlenlp import Taskflow
from tqdm import *
import pandas as pd
from save_load import save


def get_pl(data:list,
           ipt_label:list
           ):
    # 输入评论、需要踩中的关键词，返回筛选后的评论
    # 输出评论

    schema = ['品牌', '产品']

    # 设定抽取目标和定制化模型权重路径
    my_ie = Taskflow("information_extraction", schema=schema, task_path='./checkpoint/paddlenlp_120')

    ans = []
    score = []

    for i in tqdm(data):
        temp = my_ie(i)
        if temp == [{}]:
            ans.append(i)
        elif checkifin(ipt_label, temp):
            t1 = {}
            t1["ans"] = temp
            t1["text"] = i
            score.append(t1)
            ans.append(i)
    return ans, score


def checkifin(labels,ans):
    for i in labels:
        for j in ans:
            if '产品' in j:
                for k in j['产品']:
                    if i in k['text']:
                        return True
            if '品牌' in j:
                for k in j['品牌']:
                    if i in k['text']:
                        return True
    return False



schema = ['品牌', '产品']

# 设定抽取目标和定制化模型权重路径
my_ie = Taskflow("information_extraction", schema=schema, task_path='./checkpoint/paddlenlp_120')

ans = []
score = []

# 读取CSV文件
df = pd.read_csv('temp/temp.csv')

# 提取'data_here'和'label_here'列
data = df['text'].dropna().tolist()
brand = df['brand'].dropna().tolist()
product = df['product'].dropna().tolist()


for i in tqdm(data):
    temp = my_ie(i)
    if temp == [{}]:
        ans.append(i)
    else:
        check = False
        # 如果有目标产品名，保存
        for j in product:
            if j in i:
                check = True
                break
        # 如果没提到产品名，提到了目标品牌名，保存
        if '产品' not in temp[0]:
            for j in brand:
                if j in i:
                    check = True
                    break
        if check:
            ans.append(i)

save({"data": [ans], "id": ["text"]})
