from .granularity import DailyGranularity, WeeklyGranularity, MonthlyGranularity, \
    QuarterlyGranularity, YearlyGranularity


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
