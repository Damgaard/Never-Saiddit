import calendar
import os
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from never_saiddit.core.models import Job
from never_saiddit.reddit.utils import get_reddit_instance

REDDIT_QUERY_LIMIT = 10


class Command(BaseCommand):

    help = 'Program which is continually run to update jobs.'

    def authentication_exchange(self, job):
        # Hmmm.... I think this should be a user step, to confirm
        # the breaking
        r = get_reddit_instance(refresh_token=job.refresh_token)

        # Hmmm, not sure I even need this stage. Seems pretty
        # wasteful.
        print("Step: Process Authentication")

        job.state = Job.STATE_DELETING_COMMENTS
        job.save()

    def delete_comments(self, job):
        r = get_reddit_instance(refresh_token=job.refresh_token)

        comments = r.user.me().comments.new(limit=REDDIT_QUERY_LIMIT)

        # Assumption. Users are not going to create a lot of content
        # after starting the deletion process, therefore we can
        # proceed and just process the first task after started after.

        # TODO: Something needs to be done if we intend to anonymize
        # content first in the way that we select first comment to
        # alter
        print("Step: Processing comments")

        for comment in comments:
            if comment.created_utc < calendar.timegm(job.started.utctimetuple()):
                job.comments_deleted = job.comments_deleted + 1
                # Delete comment
                print(comment)
                break
        else:
            print("No comments within timeframe")
            job.state = Job.STATE_DELETING_SUBMISSIONS

        job.save()

    def delete_submissions(self, job):
        r = get_reddit_instance(refresh_token=job.refresh_token)

        submissions = r.user.me().submissions.new(limit=REDDIT_QUERY_LIMIT)

        # Assumption. Users are not going to create a lot of content
        # after starting the deletion process, therefore we can
        # proceed and just process the first task after started after.

        # TODO: Something needs to be done if we intend to anonymize
        # content first in the way that we select first submission
        # alter
        print("Step: Processing submissions")

        for submission in submissions:
            if submission.created_utc < calendar.timegm(job.started.utctimetuple()):
                job.submissions_deleted = job.submissions_deleted + 1
                # Delete submission
                print(submission)
                break
        else:
            print("No submissions within timeframe")
            job.state = Job.STATE_FINISHED

        job.save()

    def exchange_code_for_token(self, job):
        r = get_reddit_instance(refresh_token=job.refresh_token)

        print("Step: Process code")
        refresh_token = r.auth.authorize(job.code)

        job.refresh_token = refresh_token
        job.state = Job.STATE_AUTHENTICATED
        job.save()

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
        raise Exception("Tried to handle unknown state. Dunno what to do. "
                        "so lets crash.")

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
            Job.STATE_DELETING_COMMENTS: self.delete_comments,
            Job.STATE_DELETING_SUBMISSIONS: self.delete_submissions,
        }

        while not self.should_shutdown_gracefully():
            job = self.get_next_job()

            if job is None:
                step_func = self.handle_no_job
            else:
                step_func = STATE_FUNCS.get(job.state, self.handle_unknown_state)

            # TODO: Update last_updated on each iteration
            step_func(job)
