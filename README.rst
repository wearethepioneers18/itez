ITEZ
====

Platform to manage Intersex and Trans-persons in Zambia. As a Headless Backend API Service.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/cookiecutter/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: MIT

Local Dev setup
---------------

To have a running local dev environement you will need to do the following

- To build and start all services 

::

  $ docker-compose -f local.yml up

- To rebuild and start all services

::

  $ docker-compose -f local.yml up --build
  
  
*The  above command will build and start all services.*

    You can now access the web interface at http://127.0.0.1:8000
    
    You can access the api docs at http://127.0.0.1:8000/api
    
    You can access mailhog at http://127.0.0.1:8025
    
    You can access celery flower at http://127.0.0.1:5000 - user `debug` pass `debug`
    
    You can access the auto docs at http://127.0.0.1:7000

    You can access thebrowsersync UI at http://127.0.0.1:3001

- To create a superuser

::

  $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

- To update database migrations

::

  $ docker-compose -f local.yml run --rm django python manage.py makemigrations

- To apply database migrations
::

  $ docker-compose -f local.yml run --rm django python manage.py migrate


- To collect static assets

::

  $ docker-compose -f local.yml run --rm django python manage.py collectstatic


Settings
--------


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy itez

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd itez
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog

Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

Deployment
----------

The following details how to deploy this application.

Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html 


Thank You - Contributors
^^^^^^^^^

As an open source and free software, this project would not be possible without the wonderful efforts and contributions from the following talents.

- `Bupe Mulenga <https://github.com/wearethepioneers18>`_
- `Jachin Manda <https://github.com/jmnda-dev>`_
- `Chriford Siame <https://github.com/chriford>`_
- `Olipa Tembo <https://github.com/Olipa776>`_
- `Cephas Zulu <https://github.com/cazterk>`_
- `Prince Musole <https://github.com/MusoleP>`_
- Lead Engineer `Alison Mukoma <https://github.com/sonlinux>`_ <mukomalison@gmail.com>
