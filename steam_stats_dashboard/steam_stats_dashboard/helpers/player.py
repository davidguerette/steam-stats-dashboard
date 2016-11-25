'''
Player object module to handle all API calls for requested player.
May be reworked at a later time to be a proper ORM Django model.
'''
from .game import Game
from .steam_api import SteamAPI, SteamAPIInvalidUserError
from .time_calc import TimeCalc

class Player:
    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.profile_url = None
        self.persona_name = None
        self.avatar = None
        self.avatar_medium = None
        self.avatar_full = None
        self.vanity_url_name = None

        # Game collection
        self.games_owned = []

        # Private field, may not be present in profile
        self.time_joined = None

        # Load profile, game data, friend list
        self.load_profile()
        self.load_games_owned()
        self.load_friend_list()

    def __repr__(self):
        ''' String representation of Player object '''
        return "Steam User: id={0}, personaname={1}".format(self.steam_id, self.personaname)

    ################ Helper methods ################

    def load_friend_list(self):
        friend_list = SteamAPI.get_friend_list(self.steam_id).json()

        if isinstance(friend_list.get('friendslist').get('friends'), list) and \
                len(friend_list.get('friendslist').get('friends')) > 0:
            print(friend_list)

    def load_profile(self):
        ''' Load player profile data from SteamAPI GetPlayerSummaries call.
            If no value available, player attribute = None
        '''
        # TODO - implement cache
        response = SteamAPI.get_player_summaries([self.steam_id])
        profile_data = response.json()['response']['players'][0]

        self.profile_url = profile_data.get('profileurl')
        self.persona_name = profile_data.get('personaname')
        self.avatar = profile_data.get('avatar')
        self.avatar_medium = profile_data.get('avatarmedium')
        self.avatar_full = profile_data.get('avatarfull')
        self.time_joined = profile_data.get('timecreated')

    def load_games_owned(self):
        ''' Updates games_owned '''

        # TODO - implement caching
        games_owned_data = SteamAPI.get_owned_games(self.steam_id).json().get('response').get('games')

        if games_owned_data:
            # Populate list of player's games
            for game in games_owned_data:

                # Determine number of mins played over last 2 weeks
                playtime_mins_two_weeks = game['playtime_2weeks'] if 'playtime_2weeks' in game else 0

                self.games_owned.append(
                    Game(game['appid'],
                         game['name'],
                         game['img_icon_url'],
                         game['img_logo_url'],
                         game['playtime_forever'],
                         playtime_mins_two_weeks))

    ###### Time Played #######

    @property
    def time_played_total(self):
        return TimeCalc.mins_to_time_dict(self._total_playtime_mins())

    @property
    def time_played_past_two_weeks(self):
        return TimeCalc.mins_to_time_dict(self._two_week_playtime_mins())

    @property
    def avg_daily_time_lifetime(self):
        ''' Return the average number of minutes played per day
            since joining Steam, rounded to the nearest minute
        '''
        return TimeCalc.avg_time_per_day(self._total_playtime_mins(), self.time_joined)

    @property
    def avg_daily_time_two_weeks(self):
        ''' Return the average number of minutes played per day over
            the last two weeks, rounded to the nearest minute
        '''
        return TimeCalc.avg_time_per_day(self._two_week_playtime_mins(),
                                         TimeCalc.two_weeks_ago_time)

    def _total_playtime_mins(self):
        ''' Sum and return total playtime across all games for the player '''
        if not self.games_owned:
            self.load_games_owned()

        total_playtime_mins = sum(int(game.playtime_mins) for game in self.games_owned)
        return total_playtime_mins

    def _two_week_playtime_mins(self):
        ''' Return player's minutes played from the last two weeks '''
        if not self.games_owned:
            self.load_games_owned()

        return sum([int(game.playtime_mins_two_weeks) for game in self.games_owned if game.playtime_mins_two_weeks])

    ##### Game Collection Stats ####

    def calculate_collection_score(self):
        pass


    ###### Profile validation #####

    def validate_user_input_steam_id(self):
        ''' Validate the user-provided 64 bit steam_id (instance attribute) is valid
            @raises SteamAPIInvalidUserError if unable to validate user name given
        '''
        response = SteamAPI.get_player_summaries([self.steam_id])

        try:
            steam_id = response.json()['response']['players'][0]['steamid']
        except (KeyError, TypeError) as e:
            raise SteamAPIInvalidUserError("Could not validate user-input steam id: {}".format(e))

        return steam_id

    @staticmethod
    def get_steam_id_from_vanity_url_name(input_user_name):
        ''' Get user's SteamID64 from vanity url name
            @param str input_user_name: the vantiy user name associated with the user account
            @return steam_id or None

            invalid response: {'response': {'message': 'No match', 'success': 42}}
            valid response: { "response": { "steamid": "76561197969470540", "success": 1 } }
        '''
        steam_id = None
        response = SteamAPI.resolve_vanity_url(input_user_name).json()['response']

        if response.get('success') == SteamAPI.NAME_SUCCESS_MATCH and response.get('steamid'):
            steam_id = response.get('steamid')

        return steam_id
