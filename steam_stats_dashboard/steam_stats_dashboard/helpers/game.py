'''
Game object module
'''

from .time_calc import TimeCalc

class Game:
    ''' Game object class, representing a Steam game owned by a player '''
    def __init__(self, game_dict, playtime_mins_two_weeks):
        ''' Instantiate game object
            @param game_dict: data for an individual game, from full game json response
            @param int playtime_mins_two_weeks: number of mins the game has been played by
            player over the past two weeks
        '''
        self.app_id = game_dict['appid']
        self.name = game_dict['name']
        self.icon_img = game_dict['img_icon_url']
        self.logo_img = game_dict['img_logo_url']

        # Player-specific fields
        self.playtime_mins = game_dict['playtime_forever']
        self.playtime_mins_two_weeks = playtime_mins_two_weeks

    def __repr__(self):
        return "{0} - App ID: {1}".format(self.name, self.app_id)

    @property
    def time_played_total_dict(self):
        ''' Return time dict for amount of time spent in this game
            Possible time dict keys: 'years', 'weeks', 'days', 'hours', 'minutes'
        '''
        return TimeCalc.mins_to_time_dict(self.playtime_mins)

    @property
    def time_played_total_hours(self):
        ''' Convert number of mins game has been played from mins to hours '''
        return TimeCalc.hours_from_minutes(self.playtime_mins)
