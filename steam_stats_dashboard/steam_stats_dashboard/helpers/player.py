'''
Player object module to handle all API calls for requested player.
May be reworked at a later time to be a proper ORM Django model.
'''
from .game import Game
from .steam_api import SteamAPI, SteamAPIInvalidUserError
from .time_calc import TimeCalc

class Player:
    def __init__(self, steam_id, is_friend=False):
        self.steam_id = steam_id

        # Player profile fields
        self._profile_url = None
        self._persona_name = None
        self._avatar = None
        self._avatar_medium = None
        self._avatar_full = None
        self._time_joined = None # Private field, may not be present in profile
        self._vanity_url_name = None # NYI

        self.games_owned = []
        self.friend_list = []

        if is_friend:
            # Only request data when needed to reduce unnecessary API calls
            return
        else:
            self.load_profile()
            self.load_games_owned()
            self.load_friend_list()

    def __repr__(self):
        ''' String representation of Player object '''
        # return "Steam User: id={0}".format(self.steam_id)
        return "Steam User: id={0}, personaname={1}".format(self.steam_id, self.profile['persona_name'])

    @property
    def profile(self):
        ''' Return profile data as dict for JSON serialization '''
        return {
            'steam_id': self.steam_id,
            'profile_url': self._profile_url,
            'persona_name': self._persona_name,
            'avatar': self._avatar,
            'avatar_medium': self._avatar_medium,
            'avatar_full': self._avatar_full,
            'time_joined': self._time_joined,
        }

    def load_profile(self, profile_data=None):
        ''' Load player profile data from SteamAPI GetPlayerSummaries call, cache lookup,
            or provided dict profile_data. If no value available, player attribute = None
            @param dict profile_data: optional arg to pass in profile data directly
        '''

        # TODO - check cache first
        if not profile_data:
            response = SteamAPI.get_player_summaries([self.steam_id])
            profile_data = response.json()['response']['players'][0]

        self._profile_url = profile_data.get('profileurl')
        self._persona_name = profile_data.get('personaname') or "PRIVATE"
        self._avatar = profile_data.get('avatar')
        self._avatar_medium = profile_data.get('avatarmedium')
        self._avatar_full = profile_data.get('avatarfull')
        self._time_joined = profile_data.get('timecreated') # public profile only

    def load_games_owned(self):
        ''' Returns list of games (game objects) owned by Player '''

        # TODO - implement caching
        games_owned_data = SteamAPI.get_owned_games(self.steam_id).json().get('response').get('games')

        if games_owned_data:
            for game in games_owned_data:

                # Extract 2 week playtime mins and create game objects for player
                playtime_mins_two_weeks = game['playtime_2weeks'] if 'playtime_2weeks' in game else 0
                self.games_owned.append(
                    Game(game['appid'],
                         game['name'],
                         game['img_icon_url'],
                         game['img_logo_url'],
                         game['playtime_forever'],
                         playtime_mins_two_weeks))

    def load_friend_list(self):
        ''' Load a player's friend list into self.friend_list. Friends are player
            instances but with limited profile info.
            Requires two API calls: first get list of friend steam ids, then
            get profile info from those ids.
        '''

        # TODO - implement caching

        # Get basic friend data, including Steam ID
        friend_steam_ids_response = SteamAPI.get_friend_list(self.steam_id)

        friend_steam_ids = []

        if friend_steam_ids_response:
            # Get all friend steam ids
            for friend in friend_steam_ids_response.json()['friendslist']['friends']:
                friend_steam_ids.append(friend['steamid'])

            # Get profile detail for each friend using steam id
            friends_full_response = SteamAPI.get_player_summaries(friend_steam_ids).json()['response']['players']

            for friend_details in friends_full_response:
                friend = Player(friend_details['steamid'], is_friend=True)
                friend.load_profile(friend_details)
                self.friend_list.append(friend)

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
        return TimeCalc.avg_time_per_day(self._total_playtime_mins(), self._time_joined)

    @property
    def avg_daily_time_two_weeks(self):
        ''' Return the average time played per day over the last two weeks,
            rounded to the nearest minute
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

    @property
    def games_played(self):
        ''' Return list of player's games that have been played for one or more minutes '''
        return [game for game in self.games_owned if game.playtime_mins >= 1]

    @property
    def games_unplayed(self):
        ''' Return list of games that have never been played (0 mins) '''
        return [game for game in self.games_owned if game.playtime_mins == 0]

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
