'''
Player object module to handle all API calls for requested player.
May be reworked at a later time to be a proper ORM Django model.
'''
from .steam_api import SteamAPI, SteamAPIInvalidUserError

class Player:
    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.profile_url = None
        self.persona_name = None
        self.avatar = None
        self.avatar_medium = None
        self.avatar_full = None

    # ISteamUser
    def load_player_details(self):
        ''' Load player attributes from SteamAPI GetPlayerSummaries call.
            If no value available, set attribute to None
        '''
        response = SteamAPI.get_player_summaries({'steamids': self.steam_id})
        player_details = response.json()['response']['players'][0]

        self.profile_url = player_details.get('profileurl')
        self.persona_name = player_details.get('personaname')
        self.avatar = player_details.get('avatar')
        self.avatar_medium = player_details.get('avatarmedium')
        self.avatar_full = player_details.get('avatarfull')

        return player_details

    def get_player_summaries(self):
        # return SteamAPI.get_player_summaries({'steamids': self.steam_id})
        pass

    def get_friend_list(self):
        ''' Public profile only '''
        return SteamAPI.get_friend_list({'steamid': self.steam_id})

    # IPlayerService
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

    ############# Helper methods ###############

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
