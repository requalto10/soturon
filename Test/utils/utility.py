# anonymized_int : '24~29', '34~40', ...
# domain : int, その数値属性の定義域
def calc_int_IL(anonymized_int, domain):
    if not '~' in anonymized_int:
        return 0
    for i, c in enumerate(anonymized_int):
        if c == '~':
            lower_limit = int(anonymized_int[:i])
            upper_limit = int(anonymized_int[i+1:])
            break
    return (upper_limit - lower_limit) / domain


# anonymized_cat : Federal-gov~Self-emp-inc, State-gov~Self-emp-not-inc~Private
# cat_num : int, そのカテゴリデータがもつ値の種類の数, (分類木の高さ - 1)に相当
def calc_cat_IL(anonymized_cat, cat_num):
    height = 0
    for s in anonymized_cat:
        if s == '~':
            height += 1
    return height / (cat_num - 1)


# 上から順にq*ブロックのサイズを調べ、リストとして出力
# df: anonymized DataFrame
def count_blks(df):
    count = 1
    blks = []
    for id in range(1, len(df)):
        if df.at[id, 'age'] == df.at[id-1, 'age'] and df.at[id, 'education_num'] == df.at[id-1, 'education_num']:
            count += 1
        else:
            blks.append(count)
            count = 1
    blks.append(count)
    return blks


def cmp(x, y):
    if x > y:
        return 1
    elif x==y:
        return 0
    else:
        return -1


def cmp_value(element1, element2):
    if isinstance(element1, str):
        return cmp_str(element1, element2)
    else:
        return cmp(element1, element2)


def cmp_str(element1, element2):
    """
    compare number in str format correctley
    """
    try:
        return cmp(int(element1), int(element2))
    except ValueError:
        return cmp(element1, element2)


def value(x):
    '''Return the numeric type that supports addition and subtraction'''
    if isinstance(x, (int, float)):
        return float(x)
    else:
        try:
            return float(x)
        except Exception as e:
            return x


def merge_qi_value(x_left, x_right, connect_str='~'):
    '''Connect the interval boundary value as a generalized interval and return the result as a string
    return:
        result:string
    '''
    if isinstance(x_left, (int, float)):
        if x_left == x_right:
            result = '%d' % (x_left)
        else:
            result = '%d%s%d' % (x_left, connect_str, x_right)
    elif isinstance(x_left, str):
        if x_left == x_right:
            result = x_left
        else:
            result = x_left + connect_str + x_right
    elif isinstance(x_left, datetime):
        # Generalize the datetime type value
        begin_date = x_left.strftime("%Y-%m-%d %H:%M:%S")
        end_date = x_right.strftime("%Y-%m-%d %H:%M:%S")
        result = begin_date + connect_str + end_date
    return result