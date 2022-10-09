# !/usr/bin/env python
'''
Read csv data.
Support only numeric data.
Columns must be like below.
    'index', 'QI_1', 'QI_2'

'''


def read_csv(file_path, # "path_name"
        header=False,
        delimiter=',', 
        encoding="utf-8"
    ):
    
    data = []

    with open(file_path, 'r', encoding=encoding) as f:
        lines = f.readlines()
        if header:
            lines = lines[1:]
        for line in lines:
            temp_list = [item.strip() for item in line.split(delimiter)]
            QI_int_list = []
            for str_num in temp_list[1:]:
                QI_int_list.append(int(str_num))
            temp_dict = {int(temp_list[0]): QI_int_list}
            data.append(temp_dict)
        return data
