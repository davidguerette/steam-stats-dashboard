from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect

from .helpers.steam_api import SteamAPI


def home(request):
    ''' View for site home '''
    return render(request, 'home.html')

def get_steam_id_public(request):
    ''' Get user's Steam id to be used for subsequent API calls using available public profile data '''
    steam_api = SteamAPI()
    verified_steam_id = None

    steam_uid = request.GET['steam_uid']

    verified_steam_id = steam_api.get_steam_id_from_vanity_name(steam_uid)

    if verified_steam_id:
        return HttpResponse(verified_steam_id)
    else:
        return HttpResponse('could not get steam id')
