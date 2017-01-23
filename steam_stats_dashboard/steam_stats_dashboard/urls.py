"""
steam_stats_dashboard URL Configuration
"""
from django.conf.urls import include, url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/profile', views.dashboard_profile, name='dashboard'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}), # override django-allath logout
    url(r'^accounts/', include('allauth.urls')),

    # manual player lookup urls
    url(r'^get-steam-id-public/$', views.get_steam_id_public, name='get_steam_id_public'),
    url(r'^player/(?P<steam_id>[0-9]{17})$', views.player_stats, name='player_stats'),
]
