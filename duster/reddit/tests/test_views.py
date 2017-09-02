from django.core.urlresolvers import reverse
from django.utils import timezone

from test_plus.test import TestCase

from duster.core.models import Job

from ..views import AuthorizeRedirectView



class TestAuthorizeRedirectView(TestCase):

    def test_redirects(self):
        self.get('reddit:authorize')
        self.response_302()

    def test_creates_job(self):
        self.get('reddit:authorize')
        self.assertEqual(1, Job.objects.all().count())


class TestOAuthCallbackRedirectView(TestCase):

    def setUp(self):
        self.job = Job.objects.create()
        self.data = {'code': '123', 'state': self.job.identifier}

    def test_redirects(self):
        self.get('reddit:oauth_callback', data=self.data)
        self.response_302()

    def test_redirects_to_error_on_no_code(self):
        del self.data['code']
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('error'))

    def test_redirects_to_error_on_no_state(self):
        del self.data['state']
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('error'))

    def test_redirects_to_error_denied_if_so(self):
        del self.data['code']
        self.data['error'] = 'access_denied'
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('denied'))

    def test_redirects_to_error_on_unexpected_error(self):
        del self.data['code']
        self.data['error'] = 'im_a_teapot'
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('error'))

    def test_redirects_to_error_on_bad_state(self):
        self.data['state'] = "Baaaad state"
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('error'))

    def test_redirects_to_error_on_no_such_job(self):
        self.job.delete()
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('error'))

    def test_tried_to_authorize_already_started_task(self):
        self.job.state = Job.STATE_FINISHED
        self.job.save()
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('error'))

    def test_tried_to_start_old_job(self):
        self.job.started -= timezone.timedelta(minutes=120)
        self.job.save()
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('error'))

    def test_succesful_redirect(self):
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('destruction'))

    def test_succesful_updates_state(self):
        response = self.get('reddit:oauth_callback', data=self.data)
        self.assertRedirects(response, reverse('destruction'))
        reloaded_job = Job.objects.get(identifier=self.job.identifier)
        self.assertEqual(reloaded_job.state, Job.STATE_RECEIVED_CODE_AND_STATE)
