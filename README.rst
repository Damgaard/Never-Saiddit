Never-Saiddit
=============

Reclaim ownership of your content on Reddit

Purpose
-------

This project was designed to provide an easy, non-technical way of deleting
your content on Reddit.

A number of tools already exists that allow you to delete your content, but
they generally require technical knowhow, are limited to the last 1000
items, closed source or un-maintained.

With this project I aim to deliver that service, in the easiest way
requirering the least possible technical knowledge and with the highest
guarantees for privacy that can be provided. This project utilizes the
API of Reddit and can thus narrow down the scope of permissions to just
what is required and nothing more.

Setup
-----

If you wish, the project can be run locally.

Enabling Deletion
^^^^^^^^^^^^^^^^^

To protect you against you accidentally deleteting the wrong user
accounts comments and submissions during development, there are a few defense
structures built into the system.

It will not delete content during development, ie. if DEBUG is True.
The setting CAN_DELETE_CONTENT must be set to True, be default it is set to
False. To override it and set it to True, you must set the environment variable
DJANGO_CAN_DELETE_CONTENT to True as well.

Testing
-------

Run tests with the excellent py.test library

::

  $ py.test

To test coverage. A convenience method has been created, if no test errors
were encountered a HTML report will be generated as well as shown.::

    $ ./update_coverage
    $ open htmlcov/index.html

Deployment
----------

Deployment is handled seperately, and is not part of this project.
