"""
Helper module to process and generate data to be displayed in dashboard panels
"""
from .time_calc import TimeCalc

class PanelData:
    ''' Helper class for getting dashboard panel data '''

    def __init__(self, profile):
        self.profile = profile

    ###########################
    # Time played data panels #
    ###########################

    # Lifetime

    def time_played_hours_total(self):
        ''' Return total number of hours played, rounded to one decimal place '''
        return TimeCalc.hours_from_minutes(self.profile.total_playtime_mins())

    def time_played_dict_total(self):
        ''' Return ordered dict of total time played '''
        return TimeCalc.mins_to_time_dict(self.profile.total_playtime_mins())

    def avg_daily_hours_total(self):
        ''' Return average number of hours played per day '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self.profile.total_playtime_mins(), self.profile.time_joined)
        return round(avg_mins_per_day / 60, 2)

    def avg_daily_time_dict_total(self):
        ''' Return time dict of average time played per day since joining Steam.
            Possible time dict keys: 'day', 'hour', 'minute'
        '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self.profile.total_playtime_mins(), self.profile.time_joined)
        return TimeCalc.mins_to_time_dict(avg_mins_per_day)

    # Past 2 weeks

    def time_played_two_weeks_dict(self):
        ''' Return time dict from mins played over past two weeks
            Possible time dict keys: 'year', 'week', 'day', 'hour', 'minute'
        '''
        return TimeCalc.mins_to_time_dict(self.profile.two_week_playtime_mins())

    def avg_daily_time_dict_two_weeks(self):
        ''' Return time dict of average time played per day over the last two weeks.
            Possible time dict keys: 'week', 'day', 'hour', 'minute'
        '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self.profile.two_week_playtime_mins(),
                                                     TimeCalc.two_weeks_ago_time)
        return TimeCalc.mins_to_time_dict(avg_mins_per_day)
