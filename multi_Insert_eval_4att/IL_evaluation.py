import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks

def IL_calc(K):
    IL_after = 0

    index_list = [
        'age',
        'education_num',
        'id',
        'income'
    ]

    original = pd.read_csv("./insurance_data/evaluation/raw_4att.csv", names=index_list)
    df_after = pd.read_csv(f"./insurance_data/result/inserted_k={K}.csv", names=index_list)


    QI_num = 2
    data_size = len(original)

    age_domain = original['age'].max() - original['age'].min()
    educ_num_domain = original['education_num'].max() - original['education_num'].min()


    for index, record in df_after.iterrows():
        IL_after += calc_int_IL(df_after.loc[index, 'age'], age_domain)
        IL_after += calc_int_IL(df_after.loc[index, 'education_num'], educ_num_domain)

    print(f'IL_after : {IL_after}')
