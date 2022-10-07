import pandas as pd

# データセットの読み込みと使う形への整形
df =  pd.read_csv('./Mondrian/data/anonymized.csv', sep=",")
dataset_size = 1000 # エントリ数
df_resized = df.loc[:(dataset_size-1)] # 属性名以外の dataset_size 個のエントリ

# 使う匿名化後データセット：指定したエントリ数だけリスト要素をもつリスト
# [age, workclass, education-num, marital-status, occupation, race, sex, native-country, income]
#  0    1          2              3               4           5     6    7               8
list_dataset = df_resized.values.tolist()

# 数値の範囲 -> 数値のリスト　ex)['5~7'] -> [[5,6,7]]
# 今回は属性[0],[2]が数字
for i in range(len(list_dataset)):
    age = list_dataset[i][0]
    e_num = list_dataset[i][2]

    for j, c in enumerate(age):
        if c == '~':
            list_dataset[i][0] = list(range(int(age[:j]), int(age[j+1:]) + 1))

    for j, c in enumerate(e_num):
        if c == '~':
            list_dataset[i][2] = list(range(int(e_num[:j]), int(e_num[j+1:]) + 1))


# 追加エントリ
insert_entry = [18, 'Private', 6, 'Tech-support', 'Asian-Pac-Islander', 'Male', 'Japan', '<=50K']





print(len(list_dataset))

