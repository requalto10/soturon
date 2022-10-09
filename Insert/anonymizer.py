""" 
data type
[{int: [QI,QI,...]}, {int: [QI,QI,...]}...]

"""

from statistics import median


# k : int
# QI_index : 何番目のQiを partition に使用するか(0 ~ QIの数-1)
def single_dim_mondrian(data, k, QI_index):
    splitted_data = []
    block_sizes = []

    # splitVal の決定
    QI_values = []
    for record in data:
        values_index_count = 0
        for value in record.values():
            if values_index_count == QI_index:
                QI_values.append(value[QI_index])
            else:
                values_index_count += 1
    splitVal = median(QI_values) # partition に使用する閾値
        
    # data 内で lhs(>splitVal) rhs(<=splitVal) の順にレコードを並び替え
    lhs = []
    rhs = []
    for record in data:
        for value in record.values():
            if value[QI_index] > splitVal:
                lhs.append(record)
            else:
                rhs.append(record)
    splitted_data.append(lhs)
    splitted_data.append(rhs)

    return splitted_data
   
    
