'''
Game object module
'''

class Game:
    def __init__(self, app_id, name, icon_img, logo_img, playtime_mins, playtime_mins_two_weeks=0):
        self.app_id = app_id
        self.name = name
        self.icon_img = icon_img
        self.logo_img = logo_img

        # Player-specific fields
        self.playtime_mins = playtime_mins
        self.playtime_mins_two_weeks = playtime_mins_two_weeks

    def __repr__(self):
        return "{0} - App ID: {1}".format(self.name, self.app_id)
