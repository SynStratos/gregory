from gregory.util.dictionaries import *


def test_aggregate_dicts():
    input_ = [
        {'a': 1, 'b': 2},
        {'a': 2},
        {'b': 3, 'c': 1}
    ]

    res = aggregate_dicts(input_, method=sum)
    assert res == {'a': 3, 'b': 5, 'c': 1}, "Bad dictionary returned."


def test_aggregate_dicts_w_lambda():
    input_ = [
        {'a': 1, 'b': 2},
        {'a': 2},
        {'b': 3, 'c': 1}
    ]

    res = aggregate_dicts(input_, method=lambda x: round(sum(x)/max(x), 1))
    assert res == {'a': 1.5, 'b': 1.7, 'c': 1}, "Bad dictionary returned."


def test_merge_with_conflict():
    dict_sx = {'a': 1, 'b': 2}
    dict_dx = {'c': 1}

    res = merge_with_conflict(dict_sx, dict_dx)
    assert res == {'a': 1, 'b': 2, 'c': 1}, "Bad dictionary returned."

    dict_dx = {'b': 3, 'c': 1}
    try:
        _ = merge_with_conflict(dict_sx, dict_dx)
        raise AssertionError("Exception not caught.")
    except Exception:
        pass
