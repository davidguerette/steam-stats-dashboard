'''
SteamAPI constants module
'''

class Interfaces:
    ISTEAM_USER = 'ISteamUser'
    ISTEAM_USER_STATS = 'ISteamUserStats'
    IPLAYER_SERVICE = 'IPlayerService'

class Methods:
    GET_FRIEND_LIST = 'GetFriendList'
    GET_PLAYER_SUMMARIES = 'GetPlayerSummaries'
    RESOLVE_VANITY_URL = 'ResolveVanityURL'

    GET_GLOBAL_ACHIEVEMENT_PERCENTAGES_FOR_APP = 'GetGlobalAchievementPercentagesForApp'
    GET_GLOBAL_STATS_FOR_GAME = 'GetGlobalStatsForGame'
    GET_NUMBER_OF_CURRENT_PLAYERS ='GetNumberOfCurrentPlayers'
    GET_PLAYER_ACHIEVEMENTS = 'GetPlayerAchievements'
    GET_SCHEMA_FOR_GAME = 'GetSchemaForGame'
    GET_USER_STATS_FOR_GAME = 'GetUserStatsForGame'

    GET_RECENTLY_PLAYED_GAMES = 'GetRecentlyPlayedGames'
    GET_OWNED_GAMES = 'GetOwnedGames'
    GET_STEAM_LEVEL = 'GetSteamLevel'
    GET_BADGES = 'GetBadges'

class Version:
    V1 = 'v0001'
    V2 = 'v0002'
