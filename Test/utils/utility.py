# anonymized_int : '24~29', '34~40', ...
# domain : int, その数値属性の定義域
def calc_int_IL(anonymized_int, domain):
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
