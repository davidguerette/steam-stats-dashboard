"""
Helper module to process and generate data to be displayed in dashboard panels
"""
from .time_calc import TimeCalc

class PanelDataTimePlayed:
    ''' Helper class for getting time stats dashboard panel data for provided user profile '''

    def __init__(self, profile):
        self.profile = profile

    # Get time played in mins (used for other calculations)

    def _total_playtime_mins(self):
        ''' Sum and return total playtime across all games for the player '''
        return sum(int(game.playtime_mins) for game in self.profile.games_owned)

    def _two_week_playtime_mins(self):
        ''' Return player's total minutes played from the last two weeks '''
        return sum([int(game.playtime_mins_two_weeks) for game in self.profile.games_owned if game.playtime_mins_two_weeks])

    # Lifetime

    def time_played_hours_total(self):
        ''' Return total number of hours played, rounded to one decimal place '''
        return TimeCalc.hours_from_minutes(self._total_playtime_mins())

    def time_played_dict_total(self):
        ''' Return ordered dict of total time played '''
        return TimeCalc.mins_to_time_dict(self._total_playtime_mins())

    def avg_daily_hours_total(self):
        ''' Return average number of hours played per day '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self._total_playtime_mins(), self.profile.time_joined)
        return round(avg_mins_per_day / 60, 2)

    def avg_daily_time_dict_total(self):
        ''' Return time dict of average time played per day since joining Steam.
            Possible time dict keys: 'day', 'hour', 'minute'
        '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self._total_playtime_mins(), self.profile.time_joined)
        return TimeCalc.mins_to_time_dict(avg_mins_per_day)

    # Past 2 weeks

    def time_played_two_weeks_dict(self):
        ''' Return time dict from mins played over past two weeks
            Possible time dict keys: 'year', 'week', 'day', 'hour', 'minute'
        '''
        return TimeCalc.mins_to_time_dict(self._two_week_playtime_mins())

    def avg_daily_time_dict_two_weeks(self):
        ''' Return time dict of average time played per day over the last two weeks.
            Possible time dict keys: 'week', 'day', 'hour', 'minute'
        '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self._two_week_playtime_mins(),
                                                     TimeCalc.two_weeks_ago_time)
        return TimeCalc.mins_to_time_dict(avg_mins_per_day)

class PanelDataCollection:
    ''' Helper class for getting game collection panel data for provided user profile '''

    def __init__(self, profile):
        self.profile = profile

    def top_played_games(self, num_games=5):
        ''' Sort self.games_owned by number of mins played (desc) and return requested number of games
            @param int num_games: number of games to return
            @return list of game objects, ordered highest to lowest by number of minutes played
        '''
        self.profile.games_owned.sort(key=lambda x: x.playtime_mins, reverse=True)
        return self.profile.games_owned[:num_games]

    def played_and_unplayed_lists(self, played_mins_threshold=1):
        ''' Return tuple containing lists of user's played and unplayed games
            @param int played_mins_threshold: min number of minutes to classify a game as 'played'
        '''
        games_played = []
        games_unplayed = []

        for game in self.profile.games_owned:
            if game.playtime_mins >= played_mins_threshold:
                games_played.append(game)
            else:
                games_unplayed.append(game)

        return (games_played, games_unplayed)
