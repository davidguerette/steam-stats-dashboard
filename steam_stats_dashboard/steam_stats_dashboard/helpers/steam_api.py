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

class SteamAPIInvalidUserError(Exception):
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

    @classmethod
    def _build_url(cls, interface, method, version):
        return "/".join([cls.BASE_URL, interface, method, version])

    @classmethod
    def _build_params_dict(cls, params):
        ''' Returns complete params dict for request '''
        params_dict = {
            "key": settings.STEAM_API_KEY,
            "format": "json",
        }
        params_dict.update(params)

        return params_dict

    @classmethod
    def get(cls, interface, method, version, params={}):
        ''' Make a GET request to AppNexus API
            @param class const interface
            @param class const method
            @param class const version
            @param dict params
            @return response if success, None if unauthorized request
            @
        '''
        response = requests.get(cls._build_url(interface, method, version), params=params)

        if response.status_code == 200:
            return response
        elif response.status_code == 401:
            # Indicates unauthorizated request to a private profile
            return None
        else:
            raise SteamAPIInvalidResponse(response)

    @classmethod
    def post(cls, interface, method, version, data={}):
        ''' Make a POST request to Steam API '''
        return requests.post(cls._build_url(interface, method, version), data={})

    #############  ISteamUser Interface ##################

    @classmethod
    def get_player_summaries(cls, params):
        return cls.get(cls.ISTEAM_USER, cls.GET_PLAYER_SUMMARIES, 'v2', cls._build_params_dict(params))

    @classmethod
    def get_friend_list(cls, params):
        return cls.get(cls.ISTEAM_USER, cls.GET_FRIEND_LIST, 'v1', cls._build_params_dict(params))

    @classmethod
    def resolve_vanity_url(cls, params):
        return cls.get(cls.ISTEAM_USER, cls.RESOLVE_VANITY_URL, 'v1', cls._build_params_dict(params))

    #############  ISteamUserStats Interface  ##################


    #############  IPlayerService Interface ##################

    def get_owned_games(cls):
        pass

    def get_recently_played_games(cls):
        pass

    def get_steam_level(cls):
        pass

    def get_badges(cls):
        pass
