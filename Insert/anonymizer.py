""" 
data type
[{int: [QI,QI,...]}, {int: [QI,QI,...]}...]

"""

from statistics import median


# k : int
# QI_index : 何番目のQiを partition に使用するか(0 ~ QIの数-1)
def single_dim_mondrian(data, k, QI_index):
    # multi_dim_mondrianは、引数でQI_indexを指定するのではなく、再帰ごとに指定する

    if len(data) < 2*k:
        return data
    else:
        # splitVal（中央値）の決定
        QI_values = []
        for record in data:
            values_index_count = 0
            for value in record.values():
                if values_index_count == QI_index:
                    QI_values.append(value[QI_index])
                else:
                    values_index_count += 1
        splitVal = median(QI_values) # partition に使用する閾値

        # split  
        # data 内で lhs(>splitVal) rhs(<=splitVal) の順にレコードを並び替え
        lhs = []
        rhs = []
        for record in data:
            for value in record.values():
                if value[QI_index] > splitVal:
                    lhs.append(record)
                else:
                    rhs.append(record)

        # 最後の1分割でkレコード未満になるブロックができてしまったら、その分割の前の結果を返す
        if len(lhs) < k or len(rhs) < k:
            return data 
        else:
            data = single_dim_mondrian(lhs, k, QI_index) + single_dim_mondrian(rhs, k, QI_index)
            return data
   
    
