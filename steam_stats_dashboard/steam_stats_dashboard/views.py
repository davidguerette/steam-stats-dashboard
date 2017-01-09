"""
Steam Stats Dashoard views module
"""
import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .steam_api.steam_user_profile import SteamUserProfile
from .helpers.panel_data import PanelData

def home(request):
    ''' View for site home '''
    return render(request, 'home.html')

@login_required
def dashboard(request):
    ''' Dashboard view
        SteamUser's profile data accessible in template through request.user.profile.
        Other dashboard panel info in context.
    '''
    request.user.load_profile()

    if not request.user.profile.public:
        # User's profile is private, no data to display
        return render(request, 'private-profile.html')

    # get dashboard panel data
    panel_data = PanelData(request.user.profile)

    time_played = {
        'lifetime_hours': panel_data.time_played_hours_total(),
        'lifetime_time_dict': panel_data.time_played_dict_total(),
        'lifetime_daily_avg': panel_data.avg_daily_hours_total(),
        'lifetime_daily_avg_dict': panel_data.avg_daily_time_dict_total(),
    }

    # build context dict
    context = {}

    context['time_played'] = time_played

    return render(request, 'dashboard.html', context)

def get_steam_id_public(request):
    ''' Get user's Steam id to be used for subsequent API calls using available public profile data '''
    input_steam_uid = request.GET['steam_uid'].strip() # Either id or vanity user name
    steam_id = None

    # Check for user-provided steam id first
    if re.fullmatch("^[0-9]{17}$", input_steam_uid):
        # Use 64 bit Steam ID returned from API
        steam_id = SteamUserProfile(input_steam_uid).validate_user_input_steam_id()
    else:
        # Try getting steam id from vanity url name
        steam_id = SteamUserProfile.get_steam_id_from_vanity_url_name(input_steam_uid)

    if steam_id:
        return HttpResponseRedirect(reverse('player_stats', kwargs={'steam_id': steam_id}))
    else:
        return HttpResponse('could not get steam id')

def player_stats(request, steam_id):
    ''' Get and display stats for requested player '''
    player = SteamUserProfile(steam_id)
    return HttpResponse('valid player - stats page - not yet implemented')
