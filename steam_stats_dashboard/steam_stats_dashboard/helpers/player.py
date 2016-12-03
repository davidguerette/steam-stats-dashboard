'''
Player object module to handle all API calls for requested player.
May be reworked at a later time to be a proper ORM Django model.

Player usage data can only be gathered from public profiles (indicated by
communityvisibilitystate field == 3). If public_profile attribute is False,
do not attempt to load games or friend list. Private users may be displayed
as friends of other players, but display data is restricted to their personaname.
'''
from .game import Game
from .steam_api import SteamAPI, SteamAPIInvalidUserError
from .time_calc import TimeCalc

class Player:
    ''' Player class, representing a Steam user '''
    def __init__(self, steam_id, is_friend=False):
        self.steam_id = steam_id
        self.public_profile = False

        self.games_owned = []
        self.friend_list = []

        # Player profile fields
        self._profile_url = None
        self._persona_name = None
        self._avatar = None
        self._avatar_medium = None
        self._avatar_full = None
        self._time_joined = None # Private profile only
        self._vanity_url_name = None

        # Only request data for friends as needed to prevent unnecessary API calls
        if not is_friend:
            self.load_player_data()

    def __repr__(self):
        ''' String representation of Player object '''
        return "Steam User: id={0}, personaname={1}".format(self.steam_id, self.profile['persona_name'])

    @property
    def profile(self):
        ''' Return profile data as dict for JSON serialization '''
        return {
            'steam_id': self.steam_id,
            'public_profile': self.public_profile,
            'profile_url': self._profile_url,
            'persona_name': self._persona_name,
            'avatar': self._avatar,
            'avatar_medium': self._avatar_medium,
            'avatar_full': self._avatar_full,
            'time_joined': self._time_joined,
        }

    def load_player_data(self):
        ''' Fetches profile, game, and friend data for the player, and populates the profile '''
        profile_json = self.get_profile_json()
        self.load_profile(profile_json)

        # Get games and friend data if public profile
        if profile_json['communityvisibilitystate'] == SteamAPI.COMMUNITY_VISIBILITY_STATE_PUBLIC:
            games_owned_json = self.get_games_owned_json()
            self.load_games_owned(games_owned_json)

            friend_list_json = self.get_friend_list_json()
            self.load_friend_list(friend_list_json)

    ########## Get data methods ##########

    def get_profile_json(self):
        ''' Return player's profile JSON data. First, attempt to get data from cache, then API call '''

        # TODO - Implement caching

        # Get from API call
        response = SteamAPI.get_player_summaries([self.steam_id])
        profile_json = response.json()['response']['players'][0]

        return profile_json

    def get_games_owned_json(self):

        # TODO - Implement caching

        response = SteamAPI.get_owned_games(self.steam_id)
        games_owned_json = response.json()['response']['games']

        return games_owned_json

    def get_friend_list_json(self):
        ''' Return list of friends for current player that includes basic profile info, but excludes
            the friend's games_owned or friend list. This requires two requests:
            (1) get steam ids for a player's friends.
            (2) request profile info for those Steam ids.
        '''
        friend_ids = []

        # First, get list of Player's friends' Steam ids
        # TODO - Implement caching
        friend_ids_response = SteamAPI.get_friend_list(self.steam_id)

        if not friend_ids_response:
            return None

        for friend in friend_ids_response.json()['friendslist']['friends']:
            friend_ids.append(friend['steamid'])

        # Get basic profile info for each friend using friend_ids list
        # TODO - Implement caching
        friends_full_response = SteamAPI.get_player_summaries(friend_ids).json()['response']['players']

        return friends_full_response

    ########## Load Data into Profile Methods ##########

    def load_profile(self, profile_data):
        ''' Load player profile data attributes by parsing given profile_data dict.
            Set public profile attribute based on 'communityvisibilitystate' value.
            @param dict profile_data
        '''
        if profile_data['communityvisibilitystate'] == SteamAPI.COMMUNITY_VISIBILITY_STATE_PUBLIC:
            self.public_profile = True
            self._time_joined = profile_data.get('timecreated')

        self._profile_url = profile_data.get('profileurl')
        self._persona_name = profile_data.get('personaname')
        self._avatar = profile_data.get('avatar')
        self._avatar_medium = profile_data.get('avatarmedium')
        self._avatar_full = profile_data.get('avatarfull')

    def load_games_owned(self, games_owned):
        ''' Load list of games owned by Player into self.games_owned '''
        if len(games_owned) > 0:
            for game in games_owned:
                # Calculate two week playtime mins and create player Game objects
                playtime_mins_two_weeks = game['playtime_2weeks'] if 'playtime_2weeks' in game else 0
                self.games_owned.append(Game(game, playtime_mins_two_weeks))

    def load_friend_list(self, friend_list_data):
        ''' Populate self.friend_list list with player's friends.
            Ensure that is_friend=True when instantiating friend Player objects
            to defer loading their full profile info until needed
        '''
        if len(friend_list_data) > 0:
            for friend_profile_dict in friend_list_data:
                friend = Player(friend_profile_dict['steamid'], is_friend=True)

                # Now that empty friend object is created, populate its profile
                friend.load_profile(friend_profile_dict)
                self.friend_list.append(friend)

    ########## Time Played ##########

    def _total_playtime_mins(self):
        ''' Sum and return total playtime across all games for the player '''
        return sum(int(game.playtime_mins) for game in self.games_owned)

    def _two_week_playtime_mins(self):
        ''' Return player's total minutes played from the last two weeks '''
        return sum([int(game.playtime_mins_two_weeks) for game in self.games_owned if game.playtime_mins_two_weeks])

    @property
    def time_played_total_dict(self):
        ''' Return time dict from lifetime mins played
            Possible time dict keys: 'years', 'weeks', 'days', 'hours', 'minutes'
        '''
        return TimeCalc.mins_to_time_dict(self._total_playtime_mins())

    @property
    def time_played_past_two_weeks_dict(self):
        ''' Return time dict from mins played over past two weeks
            Possible time dict keys: 'years', 'weeks', 'days', 'hours', 'minutes'
        '''
        return TimeCalc.mins_to_time_dict(self._two_week_playtime_mins())

    @property
    def avg_daily_time_lifetime_dict(self):
        ''' Return time dict of average time played per day since joining Steam.
            Possible time dict keys: 'days', 'hours', 'minutes'
        '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self._total_playtime_mins(), self._time_joined)
        return TimeCalc.mins_to_time_dict(avg_mins_per_day)

    @property
    def avg_daily_time_two_weeks_dict(self):
        ''' Return time dict of average time played per day over the last two weeks.
            Possible time dict keys: 'weeks', 'days', 'hours', 'minutes'
        '''
        avg_mins_per_day = TimeCalc.avg_mins_per_day(self._two_week_playtime_mins(),
                                                     TimeCalc.two_weeks_ago_time)
        return TimeCalc.mins_to_time_dict(avg_mins_per_day)

    @property
    def time_played_total_hours(self):
        ''' Return total number of hours played, rounded to one decimal place '''
        return TimeCalc.hours_from_minutes(self._total_playtime_mins())

    ########## Game Collection Stats ##########

    @property
    def games_played(self):
        ''' Return list of player's games that have been played for one or more minutes '''
        return [game for game in self.games_owned if game.playtime_mins >= 1]

    @property
    def games_unplayed(self):
        ''' Return list of games that have never been played (0 mins) '''
        return [game for game in self.games_owned if game.playtime_mins == 0]

    @property
    def top_played_games(self, num_games=5):
        ''' Sort self.games_owned by number of mins played (desc) and return requested number of games
            @param int num_games: number of games to return
            @return list of game objects, ordered highest to lowest by number of minutes played
        '''
        self.games_owned.sort(key=lambda x: x.playtime_mins, reverse=True)
        return self.games_owned[:num_games]

    ########## Profile validation ##########

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
