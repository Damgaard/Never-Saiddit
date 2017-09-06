import praw

from django.conf import settings


def get_reddit_instance(refresh_token=None):
    """Get the interface to talk to Reddit

    :param refresh_token: The refresh token given on a previous authentication,
        which we can use to continue their session.

    """
    user_agent = ('Dust. Giving users the power to remove their content.'
                  ' Created by /u/_Daimon_')
    return praw.Reddit(user_agent=user_agent,
                       client_id=settings.REDDIT_CLIENT_ID,
                       client_secret=settings.REDDIT_CLIENT_SECRET,
                       redirect_uri=settings.REDDIT_REDIRECT_URL,
                       refresh_token=refresh_token)
