import mock

from django.test import TestCase

from never_saiddit.reddit.management.commands import update_jobs

from never_saiddit.core.models import Job


class TestUpdateJobsState(TestCase):

    """Tests for the state handling functions in the management command."""

    def setUp(self):
        self.command = update_jobs.Command()
        self.job = Job.objects.create()

    def test_authentication_exchange(self):
        self.command.authentication_exchange(self.job)

    def test_delete_content(self):
        self.command.delete_content(self.job)

    def test_exchange_code_for_token(self):
        self.command.exchange_code_for_token(self.job)

    @mock.patch.object(update_jobs.time, 'sleep')
    def test_handle_no_job(self, mocked_time):
        self.command.handle_no_job(None)
        self.assertTrue(mocked_time.called)


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


class TestUpdateJobsHandle(TestCase):

    """Tests for the handle functions in the management command."""

    def setUp(self):
        self.command = update_jobs.Command()
        self.job = Job.objects.create()

    def test_stops_on_shutdown(self):
        # If this doesn't work, this test will never terminate
        with mock.patch.object(self.command, 'should_shutdown_gracefully', return_value=True):
            with mock.patch.object(self.command, 'handle_no_job', return_value=None):
                self.command.handle()

    def test_calls_right_step_function(self):
        self.job.state = Job.STATE_RECEIVED_CODE_AND_STATE
        self.job.save()

        with mock.patch.object(self.command, 'should_shutdown_gracefully', return_value=True):
            with mock.patch.object(self.command, 'handle_no_job', return_value=None):
                with mock.patch.object(self.command, 'exchange_code_for_token') as mocked_step_function:
                    self.command.handle()
                    self.assertTrue(mocked_step_function.called)
