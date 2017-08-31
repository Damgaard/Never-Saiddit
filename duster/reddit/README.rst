Reddit
######

This app is responsible for talking to Reddits API.

Flow
^^^^

First the user clicks on a "Authorize" button, this sends the user to
reddit via a redirect on our page. The redirect stores information about
us sending us, so that later we can confirm that it was us that sent the
user to reddit.

The redirect will land the user on Reddit's authorize page, where the
user will either grant or reject our authorization. If they deny us, the
user gets redirected back to the denial_page where we can try to convice
them again. If the user accepts, they will be sent back with a state and code
as part of the GET parameters.

We confirm that the state argument is what we sent with the user, otherwise
something fishy is going on and we throw an exception.

If everything is good, then we exchange the code for a refresh token and
a access_token. We use these to authenticate as the user on reddit.

Now we have everything required to start the dusting process. The final
configuration options are stored in the database and the user is redirected to
the final page. This is a simple page, with a identifier in the url,
that via JS polling fetches information about the progress of the celery
task.
