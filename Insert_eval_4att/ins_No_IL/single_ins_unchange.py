import pandas as pd

df = pd.read_csv('../data/test/test_k=2.csv', names=('age', 'occupation', 'index', 'income'))
add_rec = pd.read_csv('../data/test/rec_to_ins.csv', names=('age', 'occupation', 'index', 'income'))
# original = pd.read_csv('./data/test/test_raw.csv', names=('age', 'occupation', 'index', 'income'))

add_age = add_rec.at[0, 'age']
add_occ = add_rec.at[0, 'occupation']



occ_num = 100  # occupationが何種類あるか
age_num = 100  # ageの範囲
where_to_add = []
age_to_add = []
occ_to_add = []

# カテゴリQI（２列目）で探す
# 対象QIのILが最小になるq*ブロックの一番上に追加レコードを挿入
""" for id in range(len(df)):
    age = df.at[id, 'age']
    occupation = df.at[id, 'occupation']
    if add_occ == occupation:
        where_to_add.append(id)
        age_to_add.append(age)
        occ_to_add.append(occupation)
        break
    elif add_occ in occupation: 
        if occupation.count('~') + 1 < occ_num:
            occ_num = occupation.count('~') + 1
            where_to_add.append(id)
            age_to_add.append(age)
            occ_to_add.append(occupation) """


# 数値QI（1列目）で探す
# 対象QIのILが最小になるq*ブロックの一番上に追加レコードを挿入
for id in range(len(df)):
    age = df.at[id, 'age']
    occupation = df.at[id, 'occupation']
    if add_age == age:
        where_to_add.append(id)
        age_to_add.append(age)
        occ_to_add.append(occupation)
        break
    else:
        ages = []
        for i, c in enumerate(age):
            if c == '~':
                ages = list(range(int(age[:i]), int(age[i+1:]) + 1))
                break
        if int(add_age) in ages:
            if len(ages) < age_num:
                age_num = len(ages)
                where_to_add.append(id)
                age_to_add.append(age)
                occ_to_add.append(occupation)


add_pos = where_to_add[-1]
df1 = df[0:add_pos]
df2 = df[add_pos:]
df1.loc[add_pos] = [age_to_add[-1], occ_to_add[-1], add_rec.at[0, 'index'], add_rec.at[0, 'income']]
df = pd.concat([df1, df2])

df = df.reset_index(drop=True)

print(df)

#df.to_csv('../data/result/ingle_inserted_no_change.csv', header=False, index=None)