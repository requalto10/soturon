import pandas as pd


df_raw = pd.read_csv('./data/evaluation/raw_9att.csv', names=index_list)
print(df_raw['age'].max() - df_raw['age'].min())
print(df_raw['education_num'].max() - df_raw['education_num'].min())



df = pd.read_csv('../Mondrian/data/adult_index_added.csv',
                 names=('age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relatioinship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'index', 'income')
                )

attribute_widths = {
    'age': df['age'].max() - df['age'].min(),
    'workclass': 8,
    'fnlwgt': df['fnlwgt'].max() - df['fnlwgt'].min(),
    'education': 16,
    'education-num': df['education-num'].max() - df['education-num'].min(),
    'marital-status': 7,
    'occupation': 14,
    'relatioinship': 6,
    'race': 5,
    'sex': 2,
    'capital-gain': df['capital-gain'].max() - df['capital-gain'].min(),
    'capital-loss': df['capital-loss'].max() - df['capital-loss'].min(),
    'hours-per-week': df['hours-per-week'].max() - df['hours-per-week'].min(),
}
# print(attribute_widths['hours-per-week'])


att_values = []
for i in range(3):
    att_values.append(set())

att_values[0].add(1)
att_values[0].add(1)
att_values[1].add(2)
# print(att_values)