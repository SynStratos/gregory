from dateutil import relativedelta as rd


class relativedelta(rd.relativedelta):
    """
    Inherits dateutil.relativedelta to add needed properties.
    """

    @property
    def total_months(self):
        return (self.years * 12) + self.months

    @property
    def total_years(self):
        return self.years + self.months/12 + self.days/365
