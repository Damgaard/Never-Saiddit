import praw

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import RedirectView

from ..core.models import Job


# Create the global reddit instance used to interact via PRAW.
# It's state will never change.
r = praw.Reddit(user_agent='Dust. Giving users the power to remove their content.'
                           ' Created by /u/_Daimon_',
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                redirect_uri=settings.REDDIT_REDIRECT_URL)


class AuthorizeRedirectView(RedirectView):
    """Redirects to authentication page on Reddit.

    This a a distinct page as we need to create a Job model before sending a
    user to reddit to ensure protection against CSRF attacks. Ie. that any
    any requests to the callback page actually originated from us and not a
    baddie. We could create a Job for every user that visited the homepage, but
    this seems quite wasteful.

    """

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        job = Job.objects.create()
        return r.auth.url(['history', 'identity', 'read'], job.identifier, "permanent")


class OAuthCallbackRedirectView(RedirectView):
    """Redirect to final task page.

    The redirect back from Reddit. Check that the state and code are valid,
    update the task with the code and redirect the user to the final task
    page.

    If the user denies us, they will be redirected to a seperate page.

    """

    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        # Confirm that we created the state, if not break it off.
        try:
            jobs = Job.objects.filter(identifier=self.request.GET.get('state', None))

            if not jobs.exists():
                return reverse('error')

        except ValueError:
            # Given state is not a UUID hex
            return reverse('error')

        job = jobs[0]
        if "error" in self.request.GET:
            # Most common case, user denied our authorization. Give
            # them a specialized error page
            if self.request.GET['error'] == "access_denied":
                job.state = Job.STATE_ACCESS_DENIED
                job.save()
                return reverse('denied')

            job.state = Job.STATE_UNKNOWN_ERROR
            job.save()
            return reverse('error')

        # Old / started task
        is_too_old = job.started + timezone.timedelta(minutes=90) < timezone.now()
        if is_too_old or job.state != Job.STATE_AUTHORIZE:
            job.state = Job.STATE_UNKNOWN_ERROR
            job.save()
            return reverse('error')

        if "code" not in self.request.GET:
            return reverse('error')

        job.state = Job.STATE_RECEIVED_CODE_AND_STATE
        job.code = self.request.GET['code']
        job.save()

        return reverse('core:destruction', kwargs={'pk': str(job.identifier)})
