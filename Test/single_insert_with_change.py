import pandas as pd

df = pd.read_csv('./data/test2/test_k=2.csv', names=('age', 'occupation', 'index', 'income'))
add_rec = pd.read_csv('./data/test2/rec_to_ins.csv', names=('age', 'occupation', 'index', 'income'))
original = pd.read_csv('./data/test2/test_raw.csv', names=('age', 'occupation', 'index', 'income'))

add_age = add_rec.at[0, 'age']
add_occ = add_rec.at[0, 'occupation']

count = 1
blks = []
k = 2

for id in range(1, len(df)):
    if df.at[id, 'age'] == df.at[id-1, 'age'] and df.at[id, 'occupation'] == df.at[id-1, 'occupation']:
        count += 1
    else:
        blks.append(count)
        count = 1
blks.append(count)


occ_num = 100  # occupationが何種類あるか
age_num = 100  # ageの範囲
where_to_add = []
age_to_add = []
occ_to_add = []

# カテゴリQI（2列目）で探す
# 追加レコードのQIを含むブロックに追加するとき、
# ブロックが２分され、片方だけ一般化を緩めた結果、両ブロックともkを満たすときだけ追加＋一般化軽減する

for i, blk_size in enumerate(blks):
    id = sum(blks[:i])  # ブロックの先頭レコードのid
    age = df.at[id, 'age']
    occupation = df.at[id, 'occupation']
    # TODO add_ageが age の範囲に入っている　かつ下のifもOKなら、に書き換える
    if add_occ in occupation:
        # ブロック内でfor文
        c = 0  # ブロック内でoccupationがadd_occと同じレコードの数
        change_rec_ids = []


        for j in range(blk_size):
            index = df.at[id + j, 'index']
            original_occ = original[original['index'] == index]['occupation']
            if add_occ == original_occ.iloc[-1]:
                c += 1
                change_rec_ids.append(id + j)

        # 2分したブロックがどちらもk個以上あるとき
        if c +1  >= k and blk_size + 1 - c >= k:
            print('splitted!')

            # add_occと'occupation'が一致する方の分割ブロックで、'occupation'をadd_occに変更する
            # つまり、change_rec_indicesに入っているindexを持つレコードの'occupation'をadd_occに変更する
            for change_id in change_rec_ids:
                x = df.loc[change_id]['age']
                y = df.loc[change_id]['index']
                z = df.loc[change_id]['income']

                df.loc[change_id] = [x, add_rec.iloc[0, 1], y, z]

            # add_recのageをブロックの値に揃える
            add_rec.iloc[0, 0] = df.iloc[id, 0]

            # add_recをブロック先頭に追加
            add_pos = id
            df1 = df[0:id]
            df2 = df[id:]

            df1.loc[id] = [add_rec.iloc[0,0], add_rec.iloc[0,1], add_rec.iloc[0,2], add_rec.iloc[0,3]]
            
            df = pd.concat([df1, df2])
            df = df.reset_index(drop=True)
    else:
        print('Cannot insert this record beause there is no record which has the same occupation.')


print(df)

#df.to_csv('./data/result/ingle_inserted_no_change.csv', header=False, index=None)