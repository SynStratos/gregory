from functools import cached_property
from datetime import date
from abc import abstractmethod, ABC

from ..util.agenda import *
from ..util.relativedelta import relativedelta


assertion_err_msg = "Given number exceeds the time range limit."


class GranularityFactory:
    @staticmethod
    def get_granularity(granularity):
        if granularity in ('daily', 'D'):
            return DailyGranularity
        elif granularity in ('weekly', 'W'):
            return WeeklyGranularity
        elif granularity in ('monthly', 'M'):
            return MonthlyGranularity
        elif granularity in ('quarterly', 'Q'):
            return QuarterlyGranularity
        elif granularity in ('yearly', 'Y'):
            return YearlyGranularity
        else:
            raise ValueError(f'Invalid granularity value: {granularity}')


class Granularity(ABC):
    """
    Abstract class used to manage time ranges of different lengths.
    """

    @abstractmethod
    def get_beginning_of_granularity(self, day: date) -> date:
        """
        Move the given date to the beginning of its granularity period.

        Example:
            (with a Monthly granularity)
            day = 2022-04-16
            returns 2022-04-01

        Args:
            day (date): Input date.

        Returns:
            date: First day of the granularity step.
        """
        pass

    @abstractmethod
    def get_end_of_granularity(self, day: date) -> date:
        """
        Move the given date to the end of its granularity period.

        Example:
            (with a Monthly granularity)
            day = 2022-04-16
            returns 2022-04-30

        Args:
            day (date): Input date.

        Returns:
            date: Last day of the granularity step.
        """
        pass

    @abstractmethod
    def __evaluate_delta__(self) -> relativedelta:
        """Calculates the time difference for the given granularity."""
        pass

    @abstractmethod
    def __assert_included_day__(self, day: date, days: int):
        """
        Checks if a range of days is included in the number of days of 
        the granularity step for the given day.

        Args:
            day (date): Reference day for the granularity step.
            days (int): Number of the days to check.
        """
        pass

    @cached_property
    def delta(self) -> relativedelta:
        """Time delta for the given granularity."""
        return self.__evaluate_delta__()

    def get_first_available_beginning(self, day: date) -> date:
        """
        Searches for the first granularity step beginning that follows a given 
        day.

        Args:
            day (date): Starting day.

        Returns:
            date: Beginning of the needed granularity.
        """
        beg = self.get_beginning_of_granularity(day)
        if beg >= day:
            return beg
        else:
            return beg + self.delta

    def get_n_day_of_granularity(self, day: date, n: int) -> date:
        """
        Move the given date to N-th day of its granularity period.

        Example:
            (with a Monthly granularity)
            day = 2022-04-16
            n = 8
            returns 2022-04-08

        Args:
            day (date): Input date.
            n (int): Number of the day to retrieve.

        Returns:
            date: N-th day of the granularity step.
        """
        self.__assert_included_day__(day=day, days=n)
        return self.get_beginning_of_granularity(day) + relativedelta(days=n-1)


class YearlyGranularity(Granularity):
    def get_beginning_of_granularity(self, day: date) -> date:
        return first_day_of_year(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_year(day)

    def __assert_included_day__(self, day: date, days: int):
        assert days <= days_of_year(day), assertion_err_msg

    def __evaluate_delta__(self) -> relativedelta:
        return relativedelta(months=12)


class QuarterlyGranularity(Granularity):
    def get_beginning_of_granularity(self, day: date):
        return first_day_of_quarter(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_quarter(day)

    def __assert_included_day__(self, day: date, days: int):
        assert days <= days_of_quarter(day), assertion_err_msg

    def __evaluate_delta__(self):
        return relativedelta(months=3)


class MonthlyGranularity(Granularity):
    def get_beginning_of_granularity(self, day: date):
        return first_day_of_month(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_month(day)

    def __assert_included_day__(self, day: date, days: int):
        assert days <= days_of_month(day), assertion_err_msg

    def __evaluate_delta__(self):
        return relativedelta(months=1)


class WeeklyGranularity(Granularity):
    def get_beginning_of_granularity(self, day: date):
        return first_day_of_week(day)

    def get_end_of_granularity(self, day: date) -> date:
        return last_day_of_week(day)

    def __assert_included_day__(self, day: date, days: int):
        assert days <= 7, assertion_err_msg

    def __evaluate_delta__(self):
        return relativedelta(weeks=1)


class DailyGranularity(Granularity):
    def __assert_included_day__(self, *args, **kwargs):
        raise AttributeError("Not available method for Daily Granularity.")

    def get_n_day_of_granularity(self, *args, **kwargs):
        raise AttributeError("Not available method for Daily Granularity.")

    def get_beginning_of_granularity(self, day: date):
        return day

    def get_end_of_granularity(self, day: date) -> date:
        return day

    def __evaluate_delta__(self):
        return relativedelta(days=1)
