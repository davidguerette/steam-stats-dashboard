from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

import re

from .helpers.player import Player
from .helpers.steam_api import SteamAPIInvalidUserError

def home(request):
    ''' View for site home '''
    return render(request, 'home.html')

def get_steam_id_public(request):
    ''' Get user's Steam id to be used for subsequent API calls using available public profile data '''
    input_steam_uid = request.GET['steam_uid'].strip() # Either id or vanity user name
    steam_id_64 = None

    # Check for user-provided steam id first
    if re.fullmatch("^[0-9]{17}$", input_steam_uid):
        # Use 64 bit Steam ID returned from API
        steam_id_64 = Player(input_steam_uid).validate_user_input_steam_id()
    else:
        # Try getting steam id from vanity url name
        steam_id_64 = Player.get_steam_id_from_vanity_url_name(input_steam_uid)

    if steam_id_64:
        return HttpResponseRedirect(reverse('player_stats', kwargs={'steam_id': steam_id_64}))
    else:
        return HttpResponse('could not get steam id')

def player_stats(request, steam_id):
    ''' Get and display stats for requested player '''
    player = Player(steam_id)
    return HttpResponse('valid player - stats page')
