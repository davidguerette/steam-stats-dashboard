'''
Steam API module

Steam API request format: http://api.steampowered.com/<interface>/<method>/<method_version>?<params>
API documentation: http://steamwebapi.azurewebsites.net
'''
from django.conf import settings
import json

import requests

from .constants import Interfaces as i, Methods as m, Version as v


class SteamAPIError(Exception):
    ''' Generic exception for SteamAPI errors '''
    pass

class SteamAPIInvalidResponse(SteamAPIError):
    pass

class SteamAPIInvalidUserError(SteamAPIError):
    pass

class SteamAPI:
    BASE_URL = "http://api.steampowered.com"
    # Interface, method, and version values for the relative url contained in constants.py

    # USER ID LOOKUP
    NAME_SUCCESS_MATCH = 1
    NAME_NO_MATCH = 42

    @classmethod
    def _build_url(cls, interface, method, version):
        return "/".join([cls.BASE_URL, interface, method, version])

    @classmethod
    def _build_params_dict(cls, params):
        ''' Add request-specific params to base params and return result dict '''
        params_dict = {
            "key": settings.STEAM_API_KEY,
            "format": "json",
        }
        params_dict.update(params)

        return params_dict

    @classmethod
    def get(cls, interface, method, version, params={}):
        ''' Make a GET request to AppNexus API
            @param const interface
            @param const method
            @param const version
            @param dict params
            @return response if success, None if unauthorized request
        '''
        response = requests.get(cls._build_url(interface, method, version), params=params)

        if response.status_code == 200:
            return response
        elif response.status_code == 401:
            # Indicates unauthorizated request to a private profile
            return None
        else:
            raise SteamAPIInvalidResponse("Invalid response. Request: {}".format(response.url))

    @classmethod
    def post(cls, interface, method, version, data={}):
        ''' Make a POST request to Steam API '''
        return requests.post(cls._build_url(interface, method, version), data={})

    #############  ISteamUser Interface ##################

    @classmethod
    def get_player_summaries(cls, steam_ids):
        ''' Get info for provided steam id(s)
            @param list steam_ids: list of id64 steam ids to retrieve profile data (100 max per request)
        '''
        if isinstance(steam_ids, list) and len(steam_ids) > 0:
            steam_id_list = ",".join(steam_ids)
            return cls.get(i.ISTEAM_USER, m.GET_PLAYER_SUMMARIES, v.V2, cls._build_params_dict({'steamids': steam_id_list}))
        else:
            raise TypeError("Must provide valid list of Steam IDs")

    @classmethod
    def get_friend_list(cls, steam_id):
        ''' Return list of friends for provided steam id '''
        return cls.get(i.ISTEAM_USER, m.GET_FRIEND_LIST, v.V1, cls._build_params_dict({"steamid": steam_id}))

    @classmethod
    def resolve_vanity_url(cls, input_user_name):
        ''' Return SteamID64 for provided vanity url name, if set up for profile '''
        return cls.get(i.ISTEAM_USER, m.RESOLVE_VANITY_URL, v.V1, cls._build_params_dict({'vanityurl': input_user_name}))

    #############  IPlayerService Interface ##################

    @classmethod
    def get_owned_games(cls, steam_id, include_played_free_games=1, include_appinfo=1):
        ''' Get list of games in library of player for steam id given.
            Includes number of minutes played per game and game-specific info
        '''
        return cls.get(i.IPLAYER_SERVICE, m.GET_OWNED_GAMES, v.V1, cls._build_params_dict({
            'steamid': steam_id,
            'include_played_free_games': include_played_free_games,
            'include_appinfo': include_appinfo
        }))

    @classmethod
    def get_recently_played_games(cls, steam_id):
        ''' Get list of recently played games (last two weeks)
            @param dict params: {"steamid": "steam_id"}
        '''
        return cls.get(i.IPLAYER_SERVICE, m.GET_RECENTLY_PLAYED_GAMES, v.V1, cls._build_params_dict({"steamid": steam_id}))

    @classmethod
    def get_steam_level(cls, steam_id):
        ''' Get a player's Steam level (Steam community metagame)
            @param dict params: {"steamid": "steam_id"}
        '''
        return cls.get(i.IPLAYER_SERVICE, m.GET_STEAM_LEVEL, v.V1, cls._build_params_dict({"steamid": steam_id}))

    @classmethod
    def get_badges(cls, steam_id):
        ''' Get list of player badges
            @param dict params: {"steamid": "steam_id"}
        '''
        return cls.get(i.IPLAYER_SERVICE, m.GET_BADGES, v.V1, cls._build_params_dict({"steamid": steam_id}))

    #############  ISteamUserStats Interface  ##################
    # METHODS NOT YET IMPLEMENTED:
    # GetGlobalAchievementPercentagesForApp
    # GetGlobalStatsForGame
    # GetNumberOfCurrentPlayers
    # GetPlayerAchievements
    # GetUserStatsForGame
