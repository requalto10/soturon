import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks
from mondrian import mondrian
import sys, copy, random
import time

# ここでkを指定
K = 10 

# データセットの読み込み
cols = ['age', 'education_num', 'a', 'b', 'c', 'd', 'e', 'index', 'income']

# 本番データ
df = pd.read_csv('./data/evaluation/k=10_9att_new.csv', names=cols)
del_rec = pd.read_csv('./data/evaluation/rec_to_del_new.csv', names=cols)
original = pd.read_csv('./data/evaluation/raw_9att.csv', names=cols)

# テストデータ
# df = pd.read_csv('./data/test3_9att_2int/test_k=3.csv', names=cols)
# del_rec = pd.read_csv('./data/test3_9att_2int/rec_to_del.csv', names=cols)
# original = pd.read_csv('./data/test3_9att_2int/test_raw.csv', names=cols)

# 各QIの数値範囲
attribute_widths = {
    'age': original['age'].max() - original['age'].min(),
    'education_num': original['education_num'].max() - original['education_num'].min(),
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
    'e': 0,
}

QI_list = ['age', 'education_num', 'a', 'b', 'c', 'd', 'e']
is_cat_list = [0, 0, 0, 0, 0, 0, 0]
INTUITIVE_ORDER = [[], [], [], [], [], [], [], []]


def get_result_qi(data, qi_num, k=5):
    k, qi_num = int(k), int(qi_num)
    # print(f"Number of QI={qi_num}")
    result, eval_result = mondrian(data, k, False, qi_num)
    result = convert_to_raw(result)
    return result


def convert_to_raw(result, connect_str='~'):
    """
    During preprocessing, categorical attributes are convert to
    numeric attribute using intuitive order. This function will convert
    these values back to they raw values. For example, Female and Male
    may be converted to 0 and 1 during anonymizaiton. Then we need to transform
    them back to original values after anonymization.
    """
    convert_result = []
    qi_len = len(INTUITIVE_ORDER)
    for record in result:
        convert_record = []
        for i in range(qi_len):
            if len(INTUITIVE_ORDER[i]) > 0:
                vtemp = ''
                if connect_str in record[i]:
                    temp = record[i].split(connect_str)
                    raw_list = []
                    for j in range(int(temp[0]), int(temp[1]) + 1):
                        raw_list.append(INTUITIVE_ORDER[i][j])
                    vtemp = connect_str.join(raw_list)
                else:
                    vtemp = INTUITIVE_ORDER[i][int(record[i])]
                convert_record.append(vtemp)
            else:
                convert_record.append(record[i])
        if isinstance(record[-1], str):
            convert_result.append(convert_record + [record[-1]])
        else:
            convert_result.append(convert_record + [connect_str.join(record[-1])])
    return convert_result


# 引数は全てDataFrame
def insert(df, add_rec, original, K):
    blks = count_blks(df)  # ブロックのサイズが上から順に格納されたリスト, ex)[3, 4, 2, ... , 3]
    IL_diff = 1000000
    blk_to_change = -1  # 追加先ブロックの先頭行インデックス
    changed_blk = pd.DataFrame(index=[], columns=cols)
    blk_size_to_change = 0

    # 全ブロックから追加先ブロックを見つける
    for i, blk_size in enumerate(blks):
        id = sum(blks[:i])  # ブロックの先頭レコードのid
        IL_before = 0
        IL_after = 0
        raw_blk = pd.DataFrame(index=[], columns=cols)  # （匿名化前）のブロックとなる空のDataFrame

        # 各レコードについてILを計算し、その合計をブロックのIL=IL_beforeとする
        for j in range(blk_size):
            index = df.at[id + j, 'index']
            record = original[original['index'] == index]
            raw_blk = pd.concat([raw_blk, record], ignore_index=True)

            # 各qiについてILを計算（IL_before）
            for x, QI in enumerate(QI_list):
                if x == 2:
                    break
                if is_cat_list[x]:  # QIがcatのとき
                    anonymized_cat = df.at[id + j, QI]
                    cat_num = attribute_widths[QI]
                    IL_before += calc_cat_IL(anonymized_cat, cat_num)
                else:  # QIがintのとき
                    anonymized_int = df.at[id + j, QI]
                    domain = attribute_widths[QI]
                    IL_before += calc_int_IL(anonymized_int, domain)

        # add_recを（匿名化前の）ブロック末尾に追加
        raw_blk = pd.concat([raw_blk, add_rec], ignore_index=True)

        raw_blk = raw_blk.values.tolist()  # DataFrameをリストに変換
        # カテゴリQIを数値に変換しないとけない

        # raw_blkにmodrianをかける
        new_blk = get_result_qi(raw_blk, len(QI_list), K) 
        new_blk = pd.DataFrame(new_blk, columns=cols)  # リストをDataFrameに変換

        # 各qiについてILを計算（IL_after）
        new_blks = count_blks(new_blk)  # new_blkに含まれるq*ブロックのサイズが上から順に格納されたリスト, ex)[3, 4, ... , 3]
        new_blks_num = len(new_blks)  # new_blkに含まれるq*ブロックの数

        for x, size in enumerate(new_blks):
            IL_add = 0
            # １レコード分のILを計算
            for y, QI in enumerate(QI_list):
                if y == 2:
                    break
                if is_cat_list[x]:  # QIがcatのとき
                    anonymized_cat = new_blk.at[sum(new_blks[:x]), QI]
                    cat_num = attribute_widths[QI]
                    IL_add += calc_cat_IL(anonymized_cat, cat_num)
                else:  # QIがintのとき
                    anonymized_int = new_blk.at[sum(new_blks[:x]), QI]
                    domain = attribute_widths[QI]
                    IL_add += calc_int_IL(anonymized_int, domain)
            # ブロックのサイズ分の合計にする
            IL_add *= size
            IL_after += IL_add

        if IL_after - IL_before < IL_diff:
            IL_diff = IL_after - IL_before
            blk_to_change = id
            changed_blk = new_blk
            blk_size_to_change = blk_size

    if blk_to_change < 0:
        print('追加できるq*ブロックがありません。')  # add_recが入れるblkが無いため、妥協したblkを探す
    else:
        drop_ids = []
        for i in range(blk_to_change, blk_to_change + blk_size_to_change):
            drop_ids.append(i)
        df = df.drop(drop_ids)
        df1 = df[0:blk_to_change]
        df2 = df[blk_to_change:]
        df = pd.concat([df1, changed_blk], ignore_index=True)
        df = pd.concat([df, df2], ignore_index=True) 

    return df   


# ここからDELETE
start_time = time.time()

del_index = del_rec.at[0,'index']
blks = count_blks(df)

head_id = -1
ungroup_blk_size = -1
del_id = df.query('index == @del_index').index[-1]

if del_id == 0:
    head_id = 0
    ungroup_blk_size = blks[0]
else:
    for i, blk_size in enumerate(blks):
        if sum(blks[:i]) > del_id:
            head_id = sum(blks[:i-1])
            ungroup_blk_size = blks[i-1]
            break

if ungroup_blk_size > K:
    df.drop(del_id, inplace=True)
    print('Deleted without ungrouping!')
else:
    ungroup_blk = df[head_id:head_id + ungroup_blk_size]
    ungroup_blk = ungroup_blk[df['index'] != del_index]  # UserWarning: Boolean Series key will be reindexed to match DataFrame index.
    df.drop(list(range(head_id, head_id + ungroup_blk_size)), inplace=True)
    df = df.reset_index(drop=True)

    for i in range(ungroup_blk_size - 1):
        anonymized_add_rec = ungroup_blk.iloc[[i], :]  # 行番号を[i]とすることでSeriesではなくDataFrameを取得
        add_rec_index = anonymized_add_rec.iat[0, 7]
        raw_add_rec = original[original['index'] == add_rec_index]
        print(f'inserting {i} th record ...')
        df = insert(df, raw_add_rec, original, K)

end_time = time.time()
print('Finish!')
print(f'Execution time: {end_time - start_time} s')
df.to_csv('./data/result/deleted_result_new.csv', header=False, index=None)
# df.to_csv('./data/result/test_deleted_result.csv', header=False, index=None)