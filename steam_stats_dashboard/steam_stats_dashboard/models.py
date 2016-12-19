from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from steam_stats_dashboard.steam_api.steam_user_profile import SteamUserProfile

class SteamUserManager(BaseUserManager):
    def create_user(self, steam_id, password=None):
        user = self.model(steam_id=steam_id)
        user.set_password(password)
        user.is_admin = False
        user.save(using=self._db)

        return user

    def create_superuser(self, steam_id, password):
        user = self.model(steam_id=steam_id)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)

        return user

class SteamUser(AbstractBaseUser):
    '''
    Custom User model containing user's steam_id
    '''
    steam_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=255) # required field for user model, but here will be unused

    profile = None

    USERNAME_FIELD = 'steam_id'

    objects = SteamUserManager()

    def __str__(self):
        return "SteamID: {}".format(self.steam_id)

    def get_full_name(self):
        return self.steam_id

    def get_short_name(self):
        return self.steam_id

    def load_profile(self):
        ''' Load user's profile information from SteamAPI '''
        if self.steam_id:
            self.profile = SteamUserProfile(self.steam_id)

    @property
    def is_staff(self):
        return self.is_admin
