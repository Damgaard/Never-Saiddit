import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import RedirectView

from ..core.models import Job
from never_saiddit.reddit.utils import get_reddit_instance




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
        r = get_reddit_instance()
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

        logger.info("Received callback for {}".format(job.identifier))

        job = jobs[0]
        if "error" in self.request.GET:
            # Most common case, user denied our authorization. Give
            # them a specialized error page
            if self.request.GET['error'] == "access_denied":
                job.state = Job.STATE_ACCESS_DENIED
                job.save()
                return reverse('denied')

            logger.error("Received unhandled error: {}".format(self.request.GET['error']))
            job.state = Job.STATE_UNKNOWN_ERROR
            job.save()
            return reverse('error')

        # Old / started task
        is_too_old = job.started + timezone.timedelta(minutes=90) < timezone.now()
        if is_too_old or job.state != Job.STATE_AUTHORIZE:
            # TODO: Add some protection against a user accidentally
            # visiting this page after deletion was started. Which
            # could set the job unneccesarily in an invalid state.
            # Perhaps this should just be redirect to some explanation page
            # or the destruction page itself?
            logger.error("Received too old / invalid state job")
            job.state = Job.STATE_UNKNOWN_ERROR
            job.save()
            return reverse('error')

        if "code" not in self.request.GET:
            logger.error("Missing code request in GET data")
            return reverse('error')

        job.state = Job.STATE_AUTHENTICATED
        job.code = self.request.GET['code']
        job.save()

        logger.error("Succesfully authenticated for job")

        return reverse('core:confirmation', kwargs={'pk': str(job.identifier)})
