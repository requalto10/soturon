"""
run mondrian with given parameters
"""

# !/usr/bin/env python
# coding=utf-8
from mondrian import mondrian
from utils.read_adult_data import read_data as read_adult
import sys, copy, random

DATA_SELECT = 'a'
RELAX = False
INTUITIVE_ORDER = None


def write_to_file(result, qi_num):
    """
    write the anonymized result to anonymized.data
    """
    with open("data/anonymized.csv", "w") as output:
        for r in result:
            output.write(','.join(r[:qi_num]) + ',' + str(r[qi_num]) + ',' + ','.join(r[qi_num+1:]) +',\n')


def get_result_qi(data, qi_num, k):
    # qi_numがsys.argv[4]で（最初からqi_num個のQIを一般化する）
    # kがsys.argv[5]になるように
    # mondrianを実行した結果をanonymized.csvとして出力

    k, qi_num = int(k), int(qi_num)
    print(f"Number of QI={qi_num}")
    result, eval_result = mondrian(data, k, RELAX, qi_num)
    if DATA_SELECT == 'a':
        result = convert_to_raw(result)
    write_to_file(result, qi_num)
    print(f"NCP {eval_result[0]:.2f}%")
    print(f"Running time {eval_result[1]:.3f} seconds")



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


if __name__ == '__main__':
    FLAG = ''
    LEN_ARGV = len(sys.argv)
    try:
        MODEL = sys.argv[1]
        DATA_SELECT = sys.argv[2]
    except IndexError:
        MODEL = 's'
        DATA_SELECT = 'a'
    INPUT_K = 10
    # read record
    if MODEL == 's':
        RELAX = False
    else:
        RELAX = True
    if RELAX:
        print("Relax Mondrian")
    else:
        print("Strict Mondrian")

    print("Adult data")
    # INTUITIVE_ORDER is an intuitive order for
    # categorical attributes. This order is produced
    # by the reading (from data set) order.
    DATA, INTUITIVE_ORDER = read_adult()
    print(INTUITIVE_ORDER)
    
    if LEN_ARGV > 3:
        FLAG = sys.argv[3]

    if FLAG == 'qi':
        get_result_qi(DATA, sys.argv[4], sys.argv[5])
    else:
        try:
            INPUT_K = int(FLAG)
            get_result_one(DATA, INPUT_K)
        except ValueError:
            print("Usage: python anonymizer [r|s] [a | i] [k | qi | data]")
            print("r: relax mondrian, s: strict mondrian")
            print("a: adult dataset, i: INFORMS dataset")
            print("k: varying k")
            print("qi: varying qi numbers")
            print("data: varying size of dataset")
            print("example: python anonymizer s a 10")
            print("example: python anonymizer s a k")
    # anonymized dataset is stored in result
    print("Finish Mondrian!!")
