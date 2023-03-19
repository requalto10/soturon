import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks
from mondrian import mondrian
import sys, copy, random
import time

# ここでkを指定
K = 2

# データセットの読み込み
cols = ['age', 'education_num', 'index', 'income']

# 本番データ
df = pd.read_csv(f'./data/evaluation/anonymized/k={K}_4att.csv', names=cols)

blks = count_blks(df)

min_size = min(blks)
min_index = blks.index(min_size)
min_where = sum(blks[:min_index]) + 1

max_size = max(blks)
max_index = blks.index(max_size)
max_where = sum(blks[:max_index]) + 1

print(f'min block size: {min_size}, where {min_where}')
print(f'max block size: {max_size}, where {max_where}')
