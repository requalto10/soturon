import pandas as pd

# データセットの読み込みと使う形への整形
df =  pd.read_csv('./Mondrian/data/anonymized.csv', sep=",")
dataset_size = 10 # エントリ数
df_resized = df.loc[:(dataset_size-1)]

# 使う匿名化後データセット：指定したエントリ数だけリスト要素をもつリスト
# [age, workclass, education-num, marital-status, occupation, race, sex, native-country, income]
#  0    1          2              3               4           5     6    7               8
list_dataset = df_resized.values.tolist()

insert_entry = [18, 'Private', 6, 'Tech-support', 'Asian-Pac-Islander', 'Male', 'Japan', '<=50K'] # 追加エントリ

# 数字の範囲 -> 数字のリスト　ex)['5~7'] -> [[5,6,7]]
for i in range(len(list_dataset)):
    age = list_dataset[i][0]
    e_num = list_dataset[i][2]

    for j, c in enumerate(age):
        if c == '~':
            list_dataset[i][0] = list(range(int(age[:j]), int(age[j+1:]) + 1))

    for j, c in enumerate(e_num):
        if c == '~':
            list_dataset[i][2] = list(range(int(e_num[:j]), int(e_num[j+1:]) + 1))

print(list_dataset)

