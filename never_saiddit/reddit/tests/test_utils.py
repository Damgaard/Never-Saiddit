from test_plus.test import TestCase

from django.test import override_settings

from never_saiddit.reddit.utils import can_delete_content, get_reddit_instance


class TestGetRedditInstance(TestCase):

    def test_instantiates(self):
        get_reddit_instance()

    @override_settings(REDDIT_CLIENT_ID=None)
    def test_raise_exception_if_not_configured(self):
        with self.assertRaises(Exception):
            get_reddit_instance()


class TestCanDeleteContent(TestCase):

    def test_returns_boolean(self):
        result = can_delete_content()
        self.assertIsInstance(result, bool)

    @override_settings(DEBUG=True)
    def test_false_in_development(self):
        result = can_delete_content()
        self.assertFalse(result)

    @override_settings(CAN_DELETE_CONTENT=False)
    def test_false_setting_not_set_to_deleting_content(self):
        result = can_delete_content()
        self.assertFalse(result)

    @override_settings(CAN_DELETE_CONTENT=True, DEBUG=False)
    def test_enabled(self):
        result = can_delete_content()
        self.assertTrue(result)
