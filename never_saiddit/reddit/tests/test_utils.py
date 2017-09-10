from test_plus.test import TestCase

from django.test import override_settings

from never_saiddit.reddit.utils import get_reddit_instance


class TestGetRedditInstance(TestCase):

    def test_instantiates(self):
        get_reddit_instance()

    @override_settings(REDDIT_CLIENT_ID=None)
    def test_raise_exception_if_not_configured(self):
        with self.assertRaises(Exception):
            get_reddit_instance()
