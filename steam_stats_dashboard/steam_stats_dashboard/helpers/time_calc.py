"""
Module to handle calculation of time stat metrics
"""
from collections import OrderedDict
import datetime
import time

SECONDS_PER_MINUTE = 60
MINS_PER_HOUR = 60
HOURS_PER_DAY = 24
DAYS_PER_WEEK = 7
DAYS_PER_YEAR = 365.25

MINS_PER_DAY = MINS_PER_HOUR * HOURS_PER_DAY
MINS_PER_WEEK = MINS_PER_DAY * DAYS_PER_WEEK
MINS_PER_YEAR = MINS_PER_DAY * DAYS_PER_YEAR

class TimeCalc:
    ''' Utility class for time conversion methods '''

    two_weeks_ago_time = time.time() - datetime.timedelta(weeks=2).total_seconds()

    @staticmethod
    def mins_to_time_dict(total_mins_played):
        ''' Create ordered dict of years, weeks, days, hours, and minutes from minutes.
            Keys take singular form to allow pluralization to happen in template filters.
            @param int total_mins_played: total number of minutes played
            @return dict time_played_dict
        '''
        time_played_dict = OrderedDict()
        mins_remainder = total_mins_played

        # Years
        time_value, mins_remainder = divmod(mins_remainder, MINS_PER_YEAR)
        if time_value:
            time_played_dict['year'] = int(time_value)

        # Weeks
        time_value, mins_remainder = divmod(mins_remainder, MINS_PER_WEEK)
        if time_value:
            time_played_dict['week'] = int(time_value)

        # Days
        time_value, mins_remainder = divmod(mins_remainder, MINS_PER_DAY)
        if time_value:
            time_played_dict['day'] = int(time_value)

        # Hours
        time_value, mins_remainder = divmod(mins_remainder, MINS_PER_HOUR)
        if time_value:
            time_played_dict['hour'] = int(time_value)

        # Minutes (remainder)
        time_played_dict['minute'] = int(mins_remainder)

        return time_played_dict

    @staticmethod
    def hours_from_minutes(mins_played):
        ''' Return number of hours from mins, rounded to one decimal place '''
        if mins_played:
            return round(mins_played / MINS_PER_HOUR, 1)
        else:
            return None

    @staticmethod
    def avg_mins_per_day(mins_played, start_time):
        ''' Return time dict containing average number of minutes or hours played
            per day since a provided start time. Round to the nearest minute.
            @param int mins_played: number of minutes played since the start time
            @param int start_time: epoch time to use as starting point for calculating average
        '''
        if mins_played:
            days_since_start_time = (time.time() - start_time) / SECONDS_PER_MINUTE / MINS_PER_DAY
            avg_mins_per_day = mins_played / days_since_start_time
        else:
            avg_mins_per_day = 0

        return avg_mins_per_day
