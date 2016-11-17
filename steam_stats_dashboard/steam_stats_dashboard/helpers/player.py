'''
Module to handle all API calls for requested player
'''
from .steam_api import SteamAPI, SteamAPIInvalidUserError

class Player:
    def __init__(self, steam_id):
        self.steam_id = steam_id

    # ISteamUser
    def load_from_steam_id(self):
        ''' Load player attributes from SteamAPI get_player_summaries call '''
        pass

    def get_player_summaries(self):
        return SteamAPI.get_player_summaries({'steamid': self.steam_id})

    def get_friend_list(self):
        ''' Public profile only '''
        return SteamAPI.get_friend_list({'steamid': self.steam_id})

    # IPlayerService
    def get_owned_games(self):
        pass

    def get_recently_played_games(self):
        pass

    def get_steam_level(self):
        pass

    def get_badges(self):
        pass


    ############# Helper methods ###############

    def validate_user_input_steam_id(self):
        ''' Validate the user-provided 64 bit steam_id (instance attribute) is valid
            @raises SteamAPIInvalidUserError if unable to validate user name given
        '''
        response = self.get_player_summaries()

        try:
            steam_id = response.json()['response']['players'][0]['steamid']
            print(steam_id)
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
