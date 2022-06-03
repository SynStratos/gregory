from typing import List


def assert_supported_aggregation(method):
    choices = ['sum', 'mean', 'max', 'min']
    e_msg = f"""Unsupported aggregation method. Available choices are '{"', '".join(choices)}' or a custom lambda)."""
    assert str(method.__name__) in choices + ['<lambda>'], e_msg


def aggregate_dicts(dicts: List[dict], method=sum) -> dict:
    """
    Given a list of dictionaries, aggregates all values in a new dictionary 
    with the given method.

    Args:
        dicts (List[dict]): Input list of dictionaries.
        method (optional): method to aggregate common values between the
        input dictionaries. Defaults to sum.

    Returns:
        dict: A single dictionary with aggregated values.
    """
    assert_supported_aggregation(method)
    keys = set([k for d in dicts for k in d.keys()])
    return {k: method([d.get(k) for d in dicts if k in d]) for k in keys}


def merge_with_conflict(a: dict, b: dict) -> dict:
    """
    Merge two dictionaries returning an error if they share any key.

    Examples:
        a = {'k1': 1, 'k2': 3}
        b = {'k3': 4, 'k4': 6}

        returns {'k1': 1, 'k2': 3, 'k3': 4, 'k4': 6}
        ------------------------------------------------------
        a = {'k1': 1, 'k2': 3}
        b = {'k1': 4, 'k4': 6}

        raises Exception for shared key 'k1'

    Args:
        a (dict): First input dictionary.
        b (dict): Second input dictionary.

    Raises:
        Exception: Raised if dictionaries share any key.

    Returns:
        dict: Resulting dictionary with merged data.
    """
    shared = set(a.keys()) & set(b.keys())
    if len(shared):
        raise Exception(
            f"Can't merge dictionaries because of shared keys [{', '.join(shared)}]")
    return {**a, **b}
