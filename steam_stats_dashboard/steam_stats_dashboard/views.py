from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

import re

from .helpers.player import Player

def home(request):
    ''' View for site home '''
    return render(request, 'home.html')

def get_steam_id_public(request):
    ''' Get user's Steam id to be used for subsequent API calls using available public profile data '''
    steam_id_64 = None
    steam_uid = request.GET['steam_uid'].strip()

    # Check for user-provided steam id first
    if re.fullmatch("^[0-9]{17}$", steam_uid):
        steam_id_64 = steam_uid
        valid = Player(steam_uid).get_player_summaries()
    else:
        # Try getting steam id from vanity url name
        steam_id_64 = Player().get_steam_id_from_vanity_name(steam_uid)

    if steam_id_64:
        return HttpResponse(steam_id_64)
    else:
        return HttpResponse('could not get steam id')

def player_stats(request):
    pass
