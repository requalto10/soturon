import pandas as pd

index_list = ['age','income','a','b','c','d','e','f','g','h','i','j','k','index','CreditCard']


df = pd.read_csv('./data/Bank_Personal_Loan_Modelling.csv', names=index_list)

for index, record in df.iterrows():
    df.loc[index, 'CreditCard'] = str(df.loc[index, 'j'])
    df.loc[index, 'index'] = str(index)
    df.loc[index, 'a'] = str(1)
    df.loc[index, 'b'] = str(1)
    df.loc[index, 'c'] = str(1)
    df.loc[index, 'd'] = str(1)
    df.loc[index, 'e'] = str(1)
    df.loc[index, 'f'] = str(1)
    df.loc[index, 'g'] = str(1)
    df.loc[index, 'h'] = str(1)
    df.loc[index, 'i'] = str(1)
    df.loc[index, 'j'] = str(1)
    df.loc[index, 'k'] = str(1)
print(df)


df.to_csv('./data/bank_index_added.csv', header=False, index=None)

