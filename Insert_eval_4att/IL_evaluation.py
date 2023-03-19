import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks


# ここでkを指定
K = 64

# 本番データ（２数値QI :age, education_num）に対するIL計算
IL_before = 0
IL_after = 0

index_list = [
    'age',
    'education_num',
    'id',
    'income'
]
# 本番データ
original = pd.read_csv("./bank_data/evaluation/raw_4att.csv", names=index_list)
df_before = pd.read_csv(f"./bank_data/evaluation/anonymized/k={K}_4att.csv", names=index_list)
df_after = pd.read_csv(f"./bank_data/result/inserted_k={K}.csv", names=index_list)


QI_num = 2
data_size = len(original)

age_domain = original['age'].max() - original['age'].min()
educ_num_domain = original['education_num'].max() - original['education_num'].min()

# print(f"age_max: {original['age'].max()}, age_min: {original['age'].min()}")
# print(f"children_max: {original['education_num'].max()}, childre_min: {original['education_num'].min()}")

for index, record in df_before.iterrows():
    IL_before += calc_int_IL(df_before.loc[index, 'age'], age_domain)
    IL_before += calc_int_IL(df_before.loc[index, 'education_num'], educ_num_domain)



for index, record in df_after.iterrows():
    IL_after += calc_int_IL(df_after.loc[index, 'age'], age_domain)
    IL_after += calc_int_IL(df_after.loc[index, 'education_num'], educ_num_domain)

print(f'IL_before : {IL_before}')
print(f'IL_after : {IL_after}\n')
print(f'NCP_average_before : {IL_before / QI_num / data_size * 100} %')
print(f'NCP_average_after : {IL_after / QI_num / data_size * 100} %')