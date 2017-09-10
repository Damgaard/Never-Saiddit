class FakeReddit(object):
    """A faked reddit instance"""

    class auth():

        def authorize(code):
            return "1234"
