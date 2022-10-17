""" 
data type
[{int: [QI,QI,...]}, {int: [QI,QI,...]}...]

"""

from curses import use_default_colors
from statistics import median
from types import NoneType

from pyparsing import rest_of_line

# １つのQIについてmondrian的にクラスタリング
# QI_index : 何番目のQiを partition に使用するか(0 ~ QIの数-1)
def single_dim_split(data, k, QI_index):
    # multi_dim_splitは、引数でQI_indexを指定するのではなく、再帰ごとに指定する

    if len(data) < 2*k:
        return data
    else:
        # splitVal（中央値）の決定
        QI_values = []
        for record in data:
            for value in record.values():
                QI_values.append(value[QI_index])
        splitVal = median(QI_values) # partition に使用する閾値

        # split  
        lhs = []
        rhs = []
        for record in data:
            for val_list in record.values():
                if val_list[QI_index] > splitVal:
                    lhs.append(record)
                else:
                    rhs.append(record)

        # 最後の1分割でkレコード未満になるブロックができてしまったら、
        # その分割の前の結果を返す
        if len(lhs) < k or len(rhs) < k:
            return data 
        else:
            data = single_dim_split(lhs, k, QI_index) + single_dim_split(rhs, k, QI_index)
            return data
   

# 同一のSA値をもつレコードを上から順にk個集めてq*ブロックとし、
# QIを、q*ブロック内にあるQI値すべてを含むリストに一般化
# data <- rest_of_records
# blocks : list of anonymized records
def simple_k_anonymizer(data, blocks=[], k=2, QI_index=0, SA_index=-1):
    used_record_keys = []
    generalized_QI_vals = []
    SA_val = list(data[0].values())[0][SA_index]
    count = 0

    for record in data:
        for key, val_list in record.items():
            print(SA_val, SA_val == val_list[SA_index])
            if SA_val == val_list[SA_index]:
                count += 1
                used_record_keys.append(key)
                if not val_list[QI_index] in generalized_QI_vals:
                    generalized_QI_vals.append(val_list[QI_index])
                if count == k:
                    break
            else:
                continue
    
    rest_of_records = []

    # これ以上ブロックを作れないとき、全レコードのQIを一般化
    if count < k:
        generalized_QI_vals = []
        keys = []
        for record in data:
            for k, val_list in record.items():
                keys.append(k)
                if not val_list[QI_index] in generalized_QI_vals:
                    generalized_QI_vals.append(val_list[QI_index])
        for key in keys:
            blocks.append({key: sorted(generalized_QI_vals)})
        return [], blocks

    for record in data:
        key = list(record.keys())[0]
        if key in used_record_keys:
            blocks.append({key: sorted(generalized_QI_vals)})
        else:
            rest_of_records.append(record)

    return simple_k_anonymizer(rest_of_records, blocks)


