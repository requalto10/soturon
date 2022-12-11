import pandas as pd

raw_index_list = [
    'age',
    'a','b','c',
    'education_num',
    'd','e','f','g','h','i','j','k',
    'id',
    'income'
]

anonymized_index_list = [
    'age',
    'a',
    'education_num',
    'b','c','d','e',
    'id',
    'income'
]

df_raw = pd.read_csv('./data/adult_index_added.csv', names=raw_index_list)
df_anonymized = pd.read_csv('./data/anonymized_k=10.csv', names=anonymized_index_list)

df_raw.drop(columns=['a','b','c','d','e','f','g','h','i','j','k'], inplace=True)
df_anonymized.drop(columns=['a','b','c','d','e'], inplace=True)

df_raw.to_csv('./data/raw.csv', header=False, index=None)
df_anonymized.to_csv('./data/k=10.csv', header=False, index=None)