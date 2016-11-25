"""
Module to handle calculation of time stat metrics
"""
import time
import datetime

MINS_PER_YEAR = 524160
MINS_PER_WEEK = 10080
MINS_PER_DAY = 1440
MINS_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
HOURS_PER_DAY = 24

class TimeCalc:
    ''' Utility class for time conversion methods '''

    two_weeks_ago_time = time.time() - datetime.timedelta(weeks=2).total_seconds()

    @staticmethod
    def mins_to_time_dict(mins_played):
        ''' Create dict of years, weeks, days, hours, and minutes from minutes
            @param int mins_played: total number of minutes played
            @return dict time_played_dict
        '''
        time_played_dict = {}

        while mins_played:
            if mins_played >= MINS_PER_YEAR:
                years = int(mins_played / MINS_PER_YEAR)
                time_played_dict['years'] = years
                mins_played -= years * MINS_PER_YEAR
            elif MINS_PER_WEEK <= mins_played < MINS_PER_YEAR:
                weeks = int(mins_played / MINS_PER_WEEK)
                time_played_dict['weeks'] = weeks
                mins_played -= weeks * MINS_PER_WEEK
            elif MINS_PER_DAY <= mins_played < MINS_PER_WEEK:
                days = int(mins_played / MINS_PER_DAY)
                time_played_dict['days'] = days
                mins_played -= days * MINS_PER_DAY
            elif MINS_PER_HOUR <= mins_played < MINS_PER_DAY:
                hours = int(mins_played / MINS_PER_HOUR)
                time_played_dict['hours'] = hours
                mins_played -= hours * MINS_PER_HOUR
            else:
                minutes = int(mins_played)
                time_played_dict['minutes'] = minutes
                mins_played -= minutes

        return time_played_dict

    @staticmethod
    def avg_time_per_day(mins_played, start_time):
        ''' Return time dict containing average number of minutes or hours played
            per day since joining Steam. Round to the nearest minute.
            @param int mins_played: number of minutes played since the start time
            @param int start_time: epoch time in seconds to use as starting point for calculating average
        '''
        days_since_joining = int(time.time() - start_time) / MINS_PER_HOUR / HOURS_PER_DAY
        avg_mins_per_day = round(mins_played / days_since_joining)

        return TimeCalc.mins_to_time_dict(avg_mins_per_day)
