from test_plus.test import TestCase

from never_saiddit.reddit.utils import get_reddit_instance


class TestGetRedditInstance(TestCase):

    def test_instantiates(self):
        get_reddit_instance()
