from test_plus.test import TestCase

from duster.core.models import Job


class TestGetJobStatus(TestCase):

    def test_no_identifier(self):
        self.get('core:get_job_status')
        self.response_404()

    def test_valid_identifier(self):
        self.job = Job.objects.create()
        self.get('core:get_job_status', data={'identifier': self.job.identifier})
        self.response_200()
