import streamlit as st
import pandas as pd
from sort import comment_sort
import datetime
from io import BytesIO


def process_file(prods, brands, file_contents):
    df = comment_sort(prods, brands, file_contents)

    # 保存结果到本地
    current_time = datetime.datetime.now()
    df.to_excel('./data/' + current_time.strftime("%Y_%m_%d %H_%M_%S") + '.xlsx', index=False)
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


# 创建文本框，用户可以输入长篇文章
user_input1 = st.text_input("请输入您的产品名称（不同昵称之间用英文分号隔开并以分号结尾）")
# 创建文本框，用户可以输入长篇文章
user_input2 = st.text_input("请输入您的产品所属的品牌名称（不同昵称之间用英文分号隔开并以分号结尾）")

# 创建文件上传功能，允许用户上传.xlsx文件
uploaded_file = st.file_uploader("请选择要上传的文件（按照第一行为列名，第一列为评论的格式）", type="xlsx")

# 检查是否有文件上传
if uploaded_file is not None:
    # file_contents = uploaded_file.read()
    file_contents = pd.read_excel(uploaded_file)

# 创建结果显示区域
result_from_file = st.empty()

# 创建按钮，分别处理文本输入和文件上传

if uploaded_file is not None and st.button('处理上传的文件'):
    prods = user_input1.split(';')[:-1]
    brands = user_input2.split(';')[:-1]
    result_from_file.text("产品名："+'、'.join(prods)+"\n品牌名："+'、'.join(brands) +
                          "\ndoc processing... please wait.")
    result_from_file.text(process_file(prods, brands, file_contents)) # 假设process_file函数会返回处理结果
