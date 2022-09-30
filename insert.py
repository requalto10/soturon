import pandas as pd
# reading csv files
data =  pd.read_csv('./Mondrian/data/anonymized.csv', sep=",")
print(data)