import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks


# 本番データ（２数値QI :age, education_num）に対するIL計算
IL_before = 0
IL_after = 0

index_list = [
    'age',
    'education_num',
    'a','b','c','d','e',
    'id',
    'income'
]

original = pd.read_csv("./data/evaluation/raw_9att.csv", names=index_list)
df_before = pd.read_csv("./data/evaluation/k=10_9att.csv", names=index_list)
df_after = pd.read_csv("./data/evaluation/inserted_result.csv", names=index_list)

age_domain = original['age'].max() - original['age'].min()
educ_num_domain = original['education_num'].max() - original['education_num'].min()


for index, record in df_before.iterrows():
    IL_before += calc_int_IL(df_before.loc[index, 'age'], age_domain)
    IL_before += calc_int_IL(df_before.loc[index, 'education_num'], educ_num_domain)

print(f'IL_before : {IL_before}')

for index, record in df_after.iterrows():
    IL_after += calc_int_IL(df_after.loc[index, 'age'], age_domain)
    IL_after += calc_int_IL(df_after.loc[index, 'education_num'], educ_num_domain)

print(f'IL_after : {IL_after}')