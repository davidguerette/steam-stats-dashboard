'''
Player object module to handle all API calls for requested player.
May be reworked at a later time to be a proper ORM Django model.
'''
from .game import Game
from .steam_api import SteamAPI, SteamAPIInvalidUserError


class Player:
    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.profile_url = None
        self.persona_name = None
        self.avatar = None
        self.avatar_medium = None
        self.avatar_full = None
        self.vanity_url_name = None
        self.games_owned = []

        # Private field, may not be present in profile
        self.timecreated = None

        # Load profile and game data
        self.load_profile()
        self.load_games_owned()

    def __repr__(self):
        ''' String representation of Player object '''
        return "Steam User: id={0}, personaname={1}".format(self.steam_id, self.personaname)

    ######### Steam API Convenience Methods ########

    def get_player_summaries(self):
        return SteamAPI.get_player_summaries({'steamids': self.steam_id})

    def get_friend_list(self):
        ''' Public profile only '''
        return SteamAPI.get_friend_list({'steamid': self.steam_id})

    def get_owned_games(self):
        return SteamAPI.get_owned_games({
            'steamid': self.steam_id,
            'include_played_free_games': 1,
            'include_appinfo': 1,
        })

    def get_recently_played_games(self):
        return SteamAPI.get_recently_played_games({'steamid': self.steam_id})

    def get_steam_level(self):
        return SteamAPI.get_steam_level({'steamid': self.steam_id})

    def get_badges(self):
        return SteamAPI.get_badges({'steamid': self.steam_id})

    # ISteamUserStats methods not yet implemented

    ################ Helper methods ################

    def load_profile(self):
        ''' Load player profile data from SteamAPI GetPlayerSummaries call.
            If no value available, player attribute = None
        '''
        # TODO - implement cache
        response = SteamAPI.get_player_summaries({'steamids': self.steam_id})
        profile_data = response.json()['response']['players'][0]

        self.profile_url = profile_data.get('profileurl')
        self.persona_name = profile_data.get('personaname')
        self.avatar = profile_data.get('avatar')
        self.avatar_medium = profile_data.get('avatarmedium')
        self.avatar_full = profile_data.get('avatarfull')
        self.date_created = profile_data.get('timecreated')

    def load_games_owned(self):
        ''' Updates games_owned '''

        # TODO - implement caching
        games_owned_data = self.get_owned_games().json().get('response').get('games')

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

    def total_playtime_mins(self):
        ''' Sum and return total playtime across all games for the player '''
        if not self.games_owned:
            self.load_games_owned()

        total_playtime_mins = sum(int(game.playtime_mins) for game in self.games_owned)
        return total_playtime_mins

    def two_week_playtime(self):
        ''' Return player's minutes played from the last two weeks '''
        if not self.games_owned:
            self.load_games_owned()

        return sum([int(game.playtime_mins_two_weeks) for game in self.games_owned if game.playtime_mins_two_weeks])

    def validate_user_input_steam_id(self):
        ''' Validate the user-provided 64 bit steam_id (instance attribute) is valid
            @raises SteamAPIInvalidUserError if unable to validate user name given
        '''
        response = self.get_player_summaries()

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
        response = SteamAPI.resolve_vanity_url({'vanityurl': input_user_name}).json()['response']

        if response.get('success') == SteamAPI.NAME_SUCCESS_MATCH and response.get('steamid'):
            steam_id = response.get('steamid')

        return steam_id
