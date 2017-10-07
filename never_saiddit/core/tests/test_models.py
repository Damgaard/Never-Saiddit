from test_plus.test import TestCase

from never_saiddit.core.models import Job


class TestJobModel(TestCase):

    def test_ordering(self):
        self.first = Job.objects.create(state=50)
        self.last = Job.objects.create(state=10)
