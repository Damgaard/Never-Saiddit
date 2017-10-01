import praw

from django.conf import settings


def get_reddit_instance(refresh_token=None):
    """Get the interface to talk to Reddit

    :param refresh_token: The refresh token given on a previous authentication,
        which we can use to continue their session.

    """
    user_agent = ('Dust. Giving users the power to remove their content.'
                  ' Created by /u/_Daimon_')
    required_attributes = [settings.REDDIT_CLIENT_ID,
                           settings.REDDIT_CLIENT_SECRET,
                           settings.REDDIT_REDIRECT_URL,
                          ]

    if any(x is None for x in required_attributes):
        raise Exception("Badly configured setup. Missing PRAW setting.")

    return praw.Reddit(user_agent=user_agent,
                       client_id=settings.REDDIT_CLIENT_ID,
                       client_secret=settings.REDDIT_CLIENT_SECRET,
                       redirect_uri=settings.REDDIT_REDIRECT_URL,
                       refresh_token=refresh_token)


def can_delete_content():
    """Return whether content should actually be deleted or just faked.

    This is used so that during development, content is not accidentally
    deployed.

    """
    return settings.CAN_DELETE_CONTENT and not settings.DEBUG
