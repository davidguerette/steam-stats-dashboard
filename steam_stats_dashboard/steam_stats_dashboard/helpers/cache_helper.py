"""
Helper module for building cache keys
"""

class CacheKey:
    USER = 'user'
    GAME = 'game'

def build_key(object_name, identifier, object_value_name):
    """
    Returns cache key name from provided params
    @param object_name: object for the key (e.g. 'user')
    @param identifier: unique id for object (typically steam_id)
    @param object_value_name: the value stored for the object (e.g. 'friend_list')

    Example result: "user:123:friend_list"
    """
    return ":".join([object_name, str(identifier), object_value_name])
