'''
Module to handle all API calls for requested player
'''
from .steam_api import SteamAPI

class Player:

    def __init__(self, steam_id=None):
        self.steam_id = steam_id
        self.steam_api = SteamAPI()

    # ISteamUser
    def get_player_summaries(self):
        params = {'steamids': self.steam_id}
        return self.steam_api.get_player_summaries(params)

    def get_friend_list(self):
        params = {'steamids': self.steam_id}
        return self.steam_api.get_friend_list(params)

    def resolve_vanity_url(self, input_user_name):
        params = {'vanityurl': input_user_name}
        return self.steam_api.resolve_vanity_url(params)

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

    def get_steam_id_from_vanity_name(self, input_user_name):
        ''' Get user's SteamID64 from vanity url name
            @param str user_name: the vantiy user name associated with the user account
            @return steam_id or None

            invalid response: {'response': {'message': 'No match', 'success': 42}}
            valid response: { "response": { "steamid": "76561197969470540", "success": 1 } }
        '''
        response = self.resolve_vanity_url(input_user_name).json()['response']

        if response.get('success') == SteamAPI.NAME_SUCCESS_MATCH and response.get('steamid'):
            steam_id = response.get('steamid')

        return steam_id or None
