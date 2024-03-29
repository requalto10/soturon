import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks
from mondrian import mondrian
import sys, copy, random
import time

# ここでkを指定
K = 4

# データセットの読み込み
cols = ['age', 'education_num', 'index', 'income']

# 本番データ
df = pd.read_csv(f'./insurance_data/evaluation/anonymized/k={K}_4att.csv', names=cols)
add_rec = pd.read_csv(f'./insurance_data/evaluation/to_insert.csv', names=cols)
original = pd.read_csv('./insurance_data/evaluation/raw_4att.csv', names=cols)

# 各QIの数値範囲
attribute_widths = {
    'age': original['age'].max() - original['age'].min(),
    'education_num': original['education_num'].max() - original['education_num'].min(),
}
QI_list = ['age', 'education_num']
is_cat_list = [0, 0]
INTUITIVE_ORDER = [[], [], []]


def get_result_qi(data, qi_num, k=5):
    k, qi_num = int(k), int(qi_num)
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
            convert_result.append(convert_record + [connect_str.join(str(record[-1]))])  # str()を入れてiterableにする応急措置
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
                if is_cat_list[y]:  # QIがcatのとき
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


start_time = time.time()
df = insert(df, add_rec, original, K)
end_time = time.time()


print('Finish!')
print(f'Execution time: {end_time - start_time} s')
df.to_csv(f'./insurance_data/result/inserted_k={K}.csv', header=False, index=None)