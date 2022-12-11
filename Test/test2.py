import pandas as pd

index_list = [
    'age',
    'education_num',
    'a','b','c','d','e',
    'id',
    'income'
]

df_raw = pd.read_csv('./data/raw.csv', names=index_list)
df_anonymized = pd.read_csv('./data/k=10.csv', names=index_list)

for index, record in df_raw.iterrows():
    df_raw.loc[index, 'a'] = '1'
    df_raw.loc[index, 'b'] = '1'
    df_raw.loc[index, 'c'] = '1'
    df_raw.loc[index, 'd'] = '1'
    df_raw.loc[index, 'e'] = '1'

for index, record in df_anonymized.iterrows():
    df_anonymized.loc[index, 'a'] = '1'
    df_anonymized.loc[index, 'b'] = '1'
    df_anonymized.loc[index, 'c'] = '1'
    df_anonymized.loc[index, 'd'] = '1'
    df_anonymized.loc[index, 'e'] = '1'


df_raw.to_csv('./data/raw_9att.csv', header=False, index=None)
df_anonymized.to_csv('./data/k=10_9att.csv', header=False, index=None)