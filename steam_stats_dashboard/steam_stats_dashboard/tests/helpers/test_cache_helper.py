"""
Unit tests for cache_helper module
"""
from django.test import TestCase

from steam_stats_dashboard.helpers.cache_helper import build_key

class TestCacheHelper(TestCase):
    """ Unit test class for cache_helper """

    def setUp(self):
        self.steam_id = '1234567890'

    def test_build_key(self):

        # Verify expected key built from valid params
        test_key_1 = build_key('user', self.steam_id, 'friend_list')
        self.assertEqual(test_key_1, 'user:1234567890:friend_list')

        # Verify expected key built when int id given
        test_key_2 = build_key('user', 1234567890, 'friend_list')
        self.assertEqual(test_key_2, 'user:1234567890:friend_list')
