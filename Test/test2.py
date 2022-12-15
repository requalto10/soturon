import pandas as pd

index_list = [
    'age',
    'education_num',
    'a','b','c','d','e',
    'index',
    'income'
]

df = pd.read_csv('./data/k=10_4att.csv', names=index_list)

for index, record in df.iterrows():
    df.loc[index, 'a'] = '1'
    df.loc[index, 'b'] = '1'
    df.loc[index, 'c'] = '1'
    df.loc[index, 'd'] = '1'
    df.loc[index, 'e'] = '1'


df.to_csv('./data/k=10_9att_new.csv', header=False, index=None)
