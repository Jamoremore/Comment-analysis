# 评论分析

## 实现功能

    评论筛选、排序、分类。

    输出数据会保存到所在目录/data文件夹下。

## 环境配置

    python版本:3.8.17
```
pip install -r requirement.txt
```

## 文件结构

| 文件名           | 功能                     |
| :--------------- | ------------------------ |
| **temp.py**      | streamlit页面创建        |
| **sort.py**      | 实现评论筛选和排序、分类 |
| **get_pl.py**    | 基于paddlenlp做评论筛选  |
| **inference.py** | 基于bert做评论排序       |
| **save_load.py** | 快速进行数据读写         |

## 实现功能

1. 评论筛选
   
   根据paddlenlp的uie模型进行关键信息提取，保留无产品和品牌信息的数据；对于余下信息，如果有目标产品名，保留；如果没有提到任何产品名，但提到目标品牌名，保留。

2. 评论排序

    根据基于BERT模型训练的评论剔除模型进行评论有效性打分，输出评论得分并降序排列。

3. 评论分类

    根据`data/dim-v2.txt`进行撞字分类。
    
## 进入指令
```
screen -r comment
```
## 网址

    http://192.168.1.155:8502

## 开启
```
screen -S comment
cd /home/datadev/leonardo/mon8/comment/streamlit-sort
conda activate llm_env
streamlit run temp.py
```

## 关闭
```
 screen -X -S comment quit
```

