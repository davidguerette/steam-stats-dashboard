"""
Auth adapter module for overriding default auth behavior
https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/adapter.py
"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class SteamSocialAuthAdapter(DefaultSocialAccountAdapter):
    ''' Override DefaultSocialAccountAdapter behavior '''

    def populate_user(self, request, sociallogin, data):
        '''
        Populate SteamUser with steam_id. Steam returns OpenID claimed id
        in format http://steamcommunity.com/openid/id/XXXXXXXXXXXXXXXXX
        where the user's actual id used for API requests is the 64 bit id
        at end of community URL.
        '''
        steam_id = sociallogin.account.uid.split('/')[-1]
        user = sociallogin.user
        user.steam_id = steam_id
        return user
