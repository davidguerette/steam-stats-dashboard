'''
Steam API module

Steam API request format: # http://api.steampowered.com/<interface>/<method>/<method_version>?<params>
API documentation: http://steamwebapi.azurewebsites.net
'''
from django.conf import settings
import requests

import json

class SteamAPIInvalidResponse(Exception):
    pass

class SteamAPI:
    BASE_URL = "http://api.steampowered.com"

    # USER ID LOOKUP
    NAME_SUCCESS_MATCH = 1
    NAME_NO_MATCH = 42

    def __init__(self):
        self.params = {
            "format": "json",
            "key": settings.STEAM_API_KEY,
        }

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

    def get_steam_id_from_vanity_name(self, user_name):
        ''' Get user's SteamID64 from vanity url name
            @param str user_name: the vantiy user name associated with the user account
            @return steam_id or None

            invalid response: {'response': {'message': 'No match', 'success': 42}}
            valid response: { "response": { "steamid": "76561197969470540", "success": 1 } }
        '''
        steam_id = None
        self.params['vanityurl'] = user_name

        response = self.get('ISteamUser', 'ResolveVanityURL', 'v0001', self.params).json()['response']

        if response.get('success') == self.NAME_SUCCESS_MATCH and response.get('steamid'):
            steam_id = response.get('steamid')

        return steam_id
