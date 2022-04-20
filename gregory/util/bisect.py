from bisect import bisect_left, bisect_right


def index_of(_list: list, value):
    """Find index of element in given list."""
    i = bisect_left(_list, value)
    try:
        assert value == _list[i], "Exact element not found."
        return i
    except (IndexError, AssertionError):
        raise ValueError


def find_lt(_list: list, value):
    """Find rightmost value less than value."""
    i = bisect_left(_list, value)
    if i:
        return _list[i-1]
    raise ValueError


def find_lte(_list: list, value):
    """Find rightmost value less than or equal to value."""
    i = bisect_right(_list, value)
    if i:
        return _list[i-1]
    raise ValueError


def find_gt(_list: list, value):
    """Find leftmost value greater than value."""
    i = bisect_right(_list, value)
    if i != len(_list):
        return _list[i]
    raise ValueError


def find_gte(_list: list, value):
    """Find leftmost item greater than or equal to value."""
    i = bisect_left(_list, value)
    if i != len(_list):
        return _list[i]
    raise ValueError


def find_delimiters(_list: list, first_element, second_element) -> tuple:
    """
    Given a list of elements, searches:
        * the index of the first element included in the given range
        * the index of the last element included in the given range

    Args:
        _list (list): Input data.
        first_element: Low limit of the range to search.
        second_element: High limit of the range to search.

    Returns:
        tuple: First and last indexes of the searched range.
    """
    idx_min = bisect_left(_list, first_element)
    idx_max = bisect_right(_list[idx_min:], second_element) + idx_min
    return idx_min, idx_max
