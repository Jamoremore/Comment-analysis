from typing import List
from tqdm import *
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from save_load import save
import pandas as pd

# 模型加载
device = 'cuda'  # 指定GPU设备
saved_model_path = 'checkpoint/check_model/model_best'  # 训练模型存放地址
tokenizer = AutoTokenizer.from_pretrained(saved_model_path)
model = AutoModelForSequenceClassification.from_pretrained(saved_model_path)
model.to(device).eval()

batch_size = 16
max_seq_len = 128

# 读取CSV文件
df = pd.read_csv('temp/temp.csv')

# 提取text列
sentences = df['text'].dropna().tolist()

res = []
for i in tqdm(range(0, len(sentences), batch_size)):
    batch_sentence = sentences[i:i+batch_size]
    ipnuts = tokenizer(
        batch_sentence,
        truncation=True,
        max_length=max_seq_len,
        padding='max_length',
        return_tensors='pt'
    )
    output = model(
        input_ids=ipnuts['input_ids'].to(device),
        token_type_ids=ipnuts['token_type_ids'].to(device),
        attention_mask=ipnuts['attention_mask'].to(device),
    ).logits
    # 先判断是概率混淆度，如果出现混淆的情况，则判定为‘其他’类
    prob = torch.softmax(output, dim=-1).cpu().tolist()
    output = [sublist[0] for sublist in prob]
    res.extend(output)

save({"data": [res, sentences], "id": ["score", "data"]})