'''
Steam API module

Steam API request format: # http://api.steampowered.com/<interface>/<method>/<method_version>?<params>
API documentation: http://steamwebapi.azurewebsites.net
'''
from django.conf import settings

import json

import requests

class SteamAPIInvalidResponse(Exception):
    pass

class SteamAPI:
    BASE_URL = "http://api.steampowered.com"

    # USER ID LOOKUP
    NAME_SUCCESS_MATCH = 1
    NAME_NO_MATCH = 42

    # INTERFACES
    ISTEAM_USER = 'ISteamUser'
    ISTEAM_USER_STATS = 'ISteamUserStats'
    IPLAYER_SERVICE = 'IPlayerService'

    # METHODS
    GET_FRIEND_LIST = 'GetFriendList'
    GET_PLAYER_SUMMARIES = 'GetPlayerSummaries'
    RESOLVE_VANITY_URL = 'ResolveVanityURL'

    GET_GLOBAL_ACHIEVEMENT_PERCENTAGES_FOR_APP = 'GetGlobalAchievementPercentagesForApp'
    GET_GLOBAL_STATS_FOR_GAME = 'GetGlobalStatsForGame'
    GET_NUMBER_OF_CURRENT_PLAYERS ='GetNumberOfCurrentPlayers'
    GET_PLAYER_ACHIEVEMENTS = 'GetPlayerAchievements'
    GET_SCHEMA_FOR_GAME = 'GetSchemaForGame'
    GET_USER_STATS_FOR_GAME = 'GetUserStatsForGame'

    GET_RECENTLY_PLAYED_GAMES = 'GetRecentlyPlayedGames'
    GET_OWNED_GAMES = 'GetOwnedGames'
    GET_STEAM_LEVEL = 'GetSteamLevel'
    GET_BADGES = 'GetBadges'

    def __init__(self):
        # All requests include format and API key params by default
        self.params = {"key": settings.STEAM_API_KEY, "format": "json"}

    def _build_url(self, interface, method, version):
        return "/".join([self.BASE_URL, interface, method, version])

    def get(self, interface, method, version, params={}):
        ''' Make a GET request to AppNexus API '''
        response = requests.get(self._build_url(interface, method, version), params=params)

        if response.status_code != 200:
            raise SteamAPIInvalidResponse(response)

        return response

    def post(self, interface, method, version, data={}):
        ''' Make a POST request to Steam API '''
        return requests.post(self._build_url(interface, method, version), data={})

    #############  ISteamUser Interface ##################

    def get_player_summaries(self, method_params):
        self.params.update(method_params)
        return self.get(self.ISTEAM_USER, self.GET_PLAYER_SUMMARIES, 'v1', self.params)

    def get_friend_list(self, method_params):
        self.params.update(method_params)
        return self.get(self.ISTEAM_USER, self.GET_FRIEND_LIST, 'v1', self.params)

    def resolve_vanity_url(self, method_params):
        self.params.update(method_params)
        return self.get(self.ISTEAM_USER, self.RESOLVE_VANITY_URL, 'v1', self.params)

    #############  ISteamUserStats Interface  ##################


    #############  IPlayerService Interface ##################

    def get_owned_games(self):
        pass

    def get_recently_played_games(self):
        pass

    def get_steam_level(self):
        pass

    def get_badges(self):
        pass
