"""
steam_stats_dashboard URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^get-steam-id-public/$', views.get_steam_id_public, name='get_steam_id_public'),
    url(r'^player/(?P<steam_id>[0-9]{17})$', views.player_stats, name='player_stats')
]
