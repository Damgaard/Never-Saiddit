import calendar
import os
import time

import praw

from django.core.management.base import BaseCommand
from django.conf import settings

from never_saiddit.core.models import Job

REDDIT_QUERY_LIMIT = 10


class Command(BaseCommand):

    help = 'Program which is continually run to update jobs.'

    def authentication_exchange(self, job):
        r = praw.Reddit(user_agent='Dust. Giving users the power to remove their content.'
                                   ' Created by /u/_Daimon_',
                        client_id=settings.REDDIT_CLIENT_ID,
                        client_secret=settings.REDDIT_CLIENT_SECRET,
                        refresh_token=job.refresh_token)

        # Hmmm, not sure I even need this stage. Seems pretty
        # wasteful.
        print("Step: Process Authentication")

        job.state = Job.STATE_DELETING_CONTENT
        job.save()

    def delete_content(self, job):
        '''
        r = praw.Reddit(user_agent='Dust. Giving users the power to remove their content.'
                                   ' Created by /u/_Daimon_',
                        client_id=settings.REDDIT_CLIENT_ID,
                        client_secret=settings.REDDIT_CLIENT_SECRET,
                        refresh_token=job.refresh_token)

        comments = r.user.me().comments.new(limit=REDDIT_QUERY_LIMIT)

        # Assumption. Users are not going to create a lot of content
        # after starting the deletion process, therefore we can
        # proceed and just process the first task after started attr.

        # TODO: Something needs to be done if we intend to anonymize
        # content first in the way that we select first comment to
        # alter
        print("Step: Processing comments")

        for comment in comments:
            if comment.created_utc < calendar.timegm(job.started.utctimetuple()):
                print(comment)
                break
        else:
            print("No comments within timeframe")
            job.state = Job.STATE_FINISHED
            job.save()
        '''
        pass

    def exchange_code_for_token(self, job):
        """
        r = praw.Reddit(user_agent='Dust. Giving users the power to remove their content.'
                                   ' Created by /u/_Daimon_',
                        client_id=settings.REDDIT_CLIENT_ID,
                        client_secret=settings.REDDIT_CLIENT_SECRET,
                        redirect_uri=settings.REDDIT_REDIRECT_URL)

        print("Step: Process code")

        refresh_token = r.auth.authorize(job.code)

        job.refresh_token = refresh_token
        job.state = Job.STATE_AUTHENTICATED
        job.save()
        """
        pass


    def should_shutdown_gracefully(self):
        """If True, this program will be terminated.

        This is to allow external shutdown of the system with putting
        anything in an invalid state.

        """

        # This approach binds us to the OS a bit more than I would normally
        # be happy with. However it solves the problem and for now we
        # can live with the binding.
        return os.path.exists('/tmp/shutdown_never_saiddt')

    def handle_unknown_state(self, job):
        """Handle a job we were given with an unknown state."""

    def get_next_job(self):
        """Return next available job for processing.

        It will return None if there are no outstanding jobs.

        """
        outstanding_jobs = Job.objects.filter(
            state__gte=Job.STATE_RECEIVED_CODE_AND_STATE,
            state__lt=Job.STATE_FINISHED,
        ).order_by('-last_updated')

        if outstanding_jobs:
            return outstanding_jobs.first()
        else:
            return None

    def handle_no_job(self, job):
        """Called when there is None.

        Strictly speaking not neccessary, but makes the structure of
        the main loop very consistent and easy to understand.

        """
        time.sleep(0.5)

    def handle(self, *args, **options):
        STATE_FUNCS = {
            Job.STATE_RECEIVED_CODE_AND_STATE: self.exchange_code_for_token,
            Job.STATE_AUTHENTICATED: self.authentication_exchange,
            Job.STATE_DELETING_CONTENT: self.delete_content,
        }

        # The function that will be called to executed this step
        step_func = None

        while True:
            job = self.get_next_job()

            if job is None:
                step_func = self.handle_no_job
            else:
                step_func = STATE_FUNCS.get(job.state, self.handle_unknown_state)

            # TODO: Update last_updated on each iteration
            step_func(job)

            if self.should_shutdown_gracefully():
                break
