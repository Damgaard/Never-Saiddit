from django.apps import AppConfig


class RedditConfig(AppConfig):
    name = 'duster.reddit'
    verbose_name = "Reddit"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
