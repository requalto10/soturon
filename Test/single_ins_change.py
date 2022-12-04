import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks

df = pd.read_csv('./data/test3/test_k=2.csv', names=('age', 'occupation', 'index', 'income'))
add_rec = pd.read_csv('./data/test3/rec_to_ins.csv', names=('age', 'occupation', 'index', 'income'))
original = pd.read_csv('./data/test3/test_raw.csv', names=('age', 'occupation', 'index', 'income'))

add_age = int(add_rec.at[0, 'age'])
add_occ = add_rec.at[0, 'occupation']

blks = count_blks(df)  # ブロックのサイズが上から順に格納されたリスト, ex)[3, 4, 2, ... , 3]

occ_num = 100  # occupationが何種類あるか（ちゃんと調べるべき）
age_num = 100  # ageの範囲（ちゃんと調べるべき）
where_to_add = []
age_to_add = []
occ_to_add = []

# カテゴリQI（2列目）で探す
# 追加レコードのQIを含むブロックに追加するとき、
# ブロックが２分され、片方だけ一般化を緩めた結果、両ブロックともkを満たすときだけ追加＋一般化軽減する

for i, blk_size in enumerate(blks):
    id = sum(blks[:i])  # ブロックの先頭レコードのid
    age = df.at[id, 'age']  # ブロックの age (str)
    occupation = df.at[id, 'occupation']  # ブロックの occupation (str)

    # age の上限と下限を求める
    if not '~' in age:
        max_age = int(age)
        min_age = -1  # 使わない age
    else:
        for n, c in enumerate(age):
            if c == '~':
                max_age = int(age[:n])
                min_age = int(age[n+1:])
                break

    #####ここから新規作成
    # まず、add_recのQIが2つとも満たされるq*ブロックを探す。

    # ageが範囲化されていないとき
    if min_age < 0:  
        if (add_age == max_age) and (add_occ in occupation):
            c = 0  # ブロック内でoccupationがadd_occと同じレコードの数
            change_rec_ids = []

            for j in range(blk_size):
                index = df.at[id + j, 'index']
                original_occ = original[original['index'] == index]['occupation']
                if add_occ == original_occ.iloc[-1]:
                    c += 1
                    change_rec_ids.append(id + j)

            add_pos = id
            df1 = df[0:id]
            df2 = df[id:]

            # 2分したブロックがどちらもk個以上あるとき
            if c +1  >= k and blk_size + 1 - c >= k:
                # change_rec_indicesに入っているindexを持つレコードの'occupation'をadd_occに変更する
                for change_id in change_rec_ids:
                    x = df.loc[change_id]['age']
                    y = df.loc[change_id]['index']
                    z = df.loc[change_id]['income']
                    df.loc[change_id] = [x, add_rec.iloc[0, 1], y, z]

                # add_recのageをブロックの値に揃える
                add_rec.iloc[0, 0] = df.iloc[id, 0]

                df1.loc[id] = [add_rec.iloc[0,0], add_rec.iloc[0,1], add_rec.iloc[0,2], add_rec.iloc[0,3]]  # ブロック先頭に追加するレコード
            # 2分したブロックの少なくともk個未満のとき
            else:
                df1.loc[id] = [add_rec.iloc[0,0], occupation, add_rec.iloc[0,2], add_rec.iloc[0,3]]  # ブロック先頭に追加するレコード  

            df = pd.concat([df1, df2])
            df = df.reset_index(drop=True)
                
    else:  # ageが範囲化されているとき
        if (min_age <= add_age <= max_age) and (add_occ in occupation):

    #####


"""     if add_occ in occupation:
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
        print('Cannot insert this record beause there is no record which has the same occupation.') """


print(df)

#df.to_csv('./data/result/ingle_inserted_no_change.csv', header=False, index=None)