from datetime import date

from .granularity import Granularity
from ..util.agenda import *


def get_first_available_beginning(
        input_granularity: Granularity,
        output_granularity: Granularity,
        day: date
) -> date:
    """
    Searches for the first (output) granularity step beginning
    that includes a given day.

    Args:
        input_granularity (Granularity): Granularity of input data.
        output_granularity (Granularity): Required output granularity.
        day (date): Starting day.

    Returns:
        date: Beginning of the needed granularity.
    """
    beg = output_granularity.get_beginning_of_granularity(day)
    if input_granularity.delta < output_granularity.delta:
        if beg >= day:
            return beg
        else:
            return beg + output_granularity.delta
    elif input_granularity.delta == output_granularity.delta:
        return beg
    else:
        raise TypeError("""Can't compare an input_granularity to an output_granularity with a greater delta.
        It is suggested to resample input data to fit the required granularity.""")
