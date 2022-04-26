from dateutil import relativedelta as rd


class relativedelta(rd.relativedelta):
    """
    Inherits dateutil.relativedelta to add needed properties.
    """
    @property
    def __total_rounded_days__(self):
        return (self.years * 365) + (self.months * 30) + self.days

    @property
    def total_months(self):
        return (self.years * 12) + self.months

    @property
    def total_years(self):
        return self.years + self.months/12 + self.days/365

    def __lt__(self, other):
        if type(other) != type(self): raise TypeError(f"'<' not supported between instances of '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        return self.__total_rounded_days__ < other.__total_rounded_days__

    def __gt__(self, other):
        if type(other) != type(self): raise TypeError(f"'>' not supported between instances of '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        return self.__total_rounded_days__ > other.__total_rounded_days__

    def __le__(self, other):
        if type(other) != type(self): raise TypeError(f"'>=' not supported between instances of '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        return self.__total_rounded_days__ <= other.__total_rounded_days__

    def __ge__(self, other):
        if type(other) != type(self): raise TypeError(f"'<=' not supported between instances of '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        return self.__total_rounded_days__ >= other.__total_rounded_days__

    def __eq__(self, other):
        if type(other) != type(self): raise TypeError(f"'==' not supported between instances of '{self.__class__.__name__}' and '{other.__class__.__name__}'")
        return self.__total_rounded_days__ == other.__total_rounded_days__
