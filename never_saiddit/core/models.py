import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Job(models.Model):

    access_token = models.CharField(
        max_length=255,
        help_text=_(
            "Used to authenticate as the user on Reddit",
        ),
    )

    refresh_token = models.CharField(
        max_length=255,
        help_text=_(
            "Used to refresh the access_token",
        ),
    )

    code = models.CharField(
        max_length=255,
        help_text=_(
            "The code given by Reddit, we use this to exchange for tokens",
        ),
    )

    started = models.DateTimeField(
        auto_now_add = True,
    )

    last_updated = models.DateTimeField(
        auto_now = True,
    )

    identifier = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        max_length=255,
        help_text=_(
            "The identifier for this task. Shown publicly.",
        ),
    )

    comments_deleted = models.PositiveSmallIntegerField(
        default=0,
    )

    submissions_deleted = models.PositiveSmallIntegerField(
        default=0,
    )

    STATE_AUTHORIZE = 10
    STATE_AUTHENTICATED = 20
    STATE_RECEIVED_CODE_AND_STATE = 30
    STATE_DELETING_COMMENTS = 40
    STATE_DELETING_SUBMISSIONS = 41
    STATE_FINISHED = 50
    STATE_UNKNOWN_ERROR = 100
    STATE_ACCESS_DENIED = 101

    # How far along in the deletion process we are. Note that there are
    # large increments to begin with, this is so that if we later on
    # decide to include additional states in between, then no additional
    # migrations will required.
    STATE_CHOICES = (
        (STATE_AUTHORIZE, _('Asked user to authorize')),
        (STATE_AUTHENTICATED, _('Authenticated as user on Reddit')),
        (STATE_RECEIVED_CODE_AND_STATE, _('Received code and state')),
        (STATE_DELETING_COMMENTS, _('Deleting comments')),
        (STATE_DELETING_SUBMISSIONS, _('Deleting submissions')),
        (STATE_FINISHED, _('Finished')),
        (STATE_UNKNOWN_ERROR, _('Unknown error')),
        (STATE_ACCESS_DENIED, _('Access denied')),
    )

    state = models.PositiveSmallIntegerField(
        choices=STATE_CHOICES,
        default=STATE_CHOICES[0][0],
        help_text=_(u"How far are we along in the process.")
    )

    class Meta:
        ordering = ['started', ]
