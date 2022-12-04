import pandas as pd
from utils.utility import calc_int_IL, calc_cat_IL, count_blks
from mondrian import mondrian
import sys, copy, random

INTUITIVE_ORDER = [[], [], [], [], [], [], [], []]

def get_result_qi(data, qi_num, k=2):
    # qi_numがsys.argv[4]で（最初からqi_num個のQIを一般化する）
    # kがsys.argv[5]になるように
    # mondrianを実行した結果をanonymized.csvとして出力

    k, qi_num = int(k), int(qi_num)
    print(f"Number of QI={qi_num}")
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


df = pd.read_csv('data/test3_9att_2int/test_k=2.csv', names=('age', 'workclass', 'education-num', 'marital-status', 'occupation', 'race', 'sex', 'index', 'income'))
add_rec = pd.read_csv('data/test3_9att_2int/rec_to_ins.csv', names=('age', 'workclass', 'education-num', 'marital-status', 'occupation', 'race', 'sex', 'index', 'income'))
original = pd.read_csv('data/test3_9att_2int/test_raw.csv', names=('age', 'workclass', 'education-num', 'marital-status', 'occupation', 'race', 'sex', 'index', 'income'))

attribute_widths = {
    'age': 7,  # ７は適当、original['age'].iloc[-1].max() - original['age'].iloc[-1].min(),
    'workclass': 8,
    'education-num': 2,  # ２は適当、original['education-num'].iloc[-1].max() - original['education-num'].iloc[-1].min(),
    'marital-status': 7,
    'occupation': 14,
    'race': 5,
    'sex': 2,
}

cols = ['age', 'workclass', 'education-num', 'marital-status', 'occupation', 'race', 'sex', 'index', 'income']
QI_list = ['age', 'workclass', 'education-num', 'marital-status', 'occupation', 'race', 'sex']
is_cat_list = [0, 1, 0, 1, 1, 1, 1]

add_age = int(add_rec.at[0, 'age'])
add_occ = add_rec.at[0, 'workclass']

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
    new_blk = get_result_qi(raw_blk, len(QI_list), 2) 
    new_blk = pd.DataFrame(new_blk, columns=cols)  # リストをDataFrameに変換

    # 各qiについてILを計算（IL_after）
    # １レコード分のILを計算
    for x, QI in enumerate(QI_list):
        if is_cat_list[x]:  # QIがcatのとき
            anonymized_cat = new_blk.at[0, QI]
            cat_num = attribute_widths[QI]
            IL_after += calc_cat_IL(anonymized_cat, cat_num)
        else:  # QIがintのとき
            anonymized_int = new_blk.at[0, QI]
            domain = attribute_widths[QI]
            IL_after += calc_int_IL(anonymized_int, domain)
    # ブロックのサイズ分の合計にする
    IL_after *= blk_size

    if IL_after - IL_before < IL_diff:
        IL_diff = IL_after - IL_before
        blk_to_change = id
        changed_blk = new_blk
        blk_size_to_change = blk_size
    print('id!!!!', blk_to_change)
print('blk_size!!!!', blk_size_to_change)


if blk_to_change < 0:
    pass  # add_recが入れるblkが無いため、妥協したblkを探す
else:
    drop_ids = []
    for i in range(id, id + blk_size_to_change + 1):
        drop_ids.append(str(i))
    print(df)
    df = df.drop(index=drop_ids)
    df1 = df[0:id]
    df2 = df[id:]
    df = pd.concat([df1, changed_blk], ignore_index=True)
    df = pd.concat([df, df2], ignore_index=True)
    

print(df)
#df.to_csv('./data/result/ingle_inserted_no_change.csv', header=False, index=None)