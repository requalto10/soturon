import pandas as pd

df = pd.read_csv('./data/test/test_k=2.csv', names=('age', 'occupation', 'index', 'income'))

df.at[0, 'index'] = 1111
occ = df.loc[df['index'] == 1111, 'occupation']
occ_x = df[df['index'] == 1111]['occupation']

print(occ[0])