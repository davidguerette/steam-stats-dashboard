"""
steam_stats_dashboard URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

# from social.apps.django_app. views import login

# import django_social_app
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^get-steam-id-public/$', views.get_steam_id_public, name='get_steam_id_public'),
    url(r'^player/(?P<steam_id>[0-9]{17})$', views.player_stats, name='player_stats'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^logged-in/$', views.logged_in, name='logged_id_view'),
]
