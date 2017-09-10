import mock

from django.test import TestCase

from never_saiddit.reddit.management.commands import update_jobs
from never_saiddit.reddit.tests.utils import FakeReddit

from never_saiddit.core.models import Job


class TestUpdateJobsState(TestCase):

    """Tests for the state handling functions in the management command."""

    def setUp(self):
        self.command = update_jobs.Command()
        self.job = Job.objects.create()

    def test_authentication_exchange(self):
        self.command.authentication_exchange(self.job)

    @mock.patch.object(update_jobs, 'get_reddit_instance', return_value=FakeReddit)
    def test_exchange_code_for_token(self, faked_reddit_instance):
        self.command.exchange_code_for_token(self.job)

    @mock.patch.object(update_jobs.time, 'sleep')
    def test_handle_no_job(self, mocked_time):
        self.command.handle_no_job(None)
        self.assertTrue(mocked_time.called)

    def test_handle_unknown_state(self):
        with self.assertRaises(Exception):
            self.command.handle_unknown_state(self.job)


class TestUpdateJobsGeneral(TestCase):

    """Tests for the general functions in the management command."""

    def setUp(self):
        self.command = update_jobs.Command()

    def test_get_next_job_no_jobs(self):
        result = self.command.get_next_job()
        self.assertIsNone(result)

    def test_get_next_job_job(self):
        self.job = Job.objects.create(state=Job.STATE_RECEIVED_CODE_AND_STATE)
        result = self.command.get_next_job()
        self.assertEqual(result, self.job)

    def test_should_shutdown(self):
        with mock.patch.object(update_jobs.os.path, 'exists', return_value=True):
            result = self.command.should_shutdown_gracefully()


def _stop_on_second_execution_wrapper(wrapped_function):
    """Wraps a test, so that the main loop terminates after 1 iteration."""

    def wrapper(self, *args, **kwargs):
        def false_then_true(*args):
            def second_call(*args):
                return True
            mocked_shutdown.side_effect = second_call
            return False

        with mock.patch.object(self.command, 'should_shutdown_gracefully', side_effect=false_then_true) as mocked_shutdown:
            with mock.patch.object(self.command, 'handle_no_job', return_value=None):
                return wrapped_function(self, *args, **kwargs)

    return wrapper

class TestUpdateJobsHandle(TestCase):

    """Tests for the handle functions in the management command."""

    def setUp(self):
        self.command = update_jobs.Command()
        self.job = Job.objects.create()

    def test_terminates_if_asked_to_shutdown(self):
        # If this doesn't work, this test will never terminate
        with mock.patch.object(self.command, 'should_shutdown_gracefully', return_value=True):
            self.command.handle()

    @_stop_on_second_execution_wrapper
    def test_no_job(self):
        self.job.delete()

        with mock.patch.object(self.command, 'handle_no_job') as mocked_step_function:
            self.command.handle()
            self.assertTrue(mocked_step_function.called)

    @_stop_on_second_execution_wrapper
    def test_calls_right_step_function(self):
        self.job.state = Job.STATE_RECEIVED_CODE_AND_STATE
        self.job.save()

        with mock.patch.object(self.command, 'exchange_code_for_token') as mocked_step_function:
            self.command.handle()
            self.assertTrue(mocked_step_function.called)
