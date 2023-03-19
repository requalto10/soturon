import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks

index_list = [
    'age',
    'education_num',
    'a','b','c','d','e',
    'id',
    'income'
]

df = pd.read_csv('./data/evaluation/k=10_9att_new.csv', names=index_list)
blks = count_blks(df)
print(blks[1:])
for i in blks:
    if i < 10:
        print('blk_sizeが10未満になっとるがな!')
print('正常')



# df = pd.read_csv('../Mondrian/data/adult_index_added.csv',
#                  names=('age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relatioinship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'index', 'income')
#                 )

# attribute_widths = {
#     'age': df['age'].max() - df['age'].min(),
#     'workclass': 8,
#     'fnlwgt': df['fnlwgt'].max() - df['fnlwgt'].min(),
#     'education': 16,
#     'education-num': df['education-num'].max() - df['education-num'].min(),
#     'marital-status': 7,
#     'occupation': 14,
#     'relatioinship': 6,
#     'race': 5,
#     'sex': 2,
#     'capital-gain': df['capital-gain'].max() - df['capital-gain'].min(),
#     'capital-loss': df['capital-loss'].max() - df['capital-loss'].min(),
#     'hours-per-week': df['hours-per-week'].max() - df['hours-per-week'].min(),
# }
# # print(attribute_widths['hours-per-week'])


# att_values = []
# for i in range(3):
#     att_values.append(set())

# att_values[0].add(1)
# att_values[0].add(1)
# att_values[1].add(2)
# # print(att_values)