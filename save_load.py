import pandas as pd


def save(data):
    max_len = max([len(i) for i in data["data"]])

    temp = {}
    for i in range(len(data["data"])):
        temp[data["id"][i]] = data["data"][i]+[float("NaN")] * (max_len - len(data["data"][i]))
    df = pd.DataFrame(temp)

    df.to_csv('./temp/temp.csv', index=False)

