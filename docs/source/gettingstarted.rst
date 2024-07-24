Getting Started
===============

.. index:: pip, virtualenv, PostgreSQL

Setting Up Development Environment
----------------------------------

Make sure to have the following on your host:

* Python 3.12
* PostgreSQL_
* Cookiecutter_
* AwsCLI_

First things first.

#. Create a virtualenv: ::

    $ python3.12 -m venv <virtual env path>

#. Activate the virtualenv you have just created: ::

    $ source <virtual env path>/bin/activate

#.
    .. include:: generate-project-block.rst

#. Install development requirements: ::

    $ cd <what you have entered as the project_slug at setup stage>
    $ pip install -r requirements/local.txt
    $ git init # A git repo is required for pre-commit to install
    $ pre-commit install

   .. note::

       The `pre-commit` hook exists in the generated project as default.
       For the details of `pre-commit`, follow the `pre-commit`_ site.

#. Create a new PostgreSQL database using createdb_: ::

    $ createdb --username=postgres <project_slug>

   ``project_slug`` is what you have entered as the project_slug at the setup stage.

   .. note::

       If this is the first time a database is created on your machine you might need an
       `initial PostgreSQL set up`_ to allow local connections & set a password for
       the ``postgres`` user. The `postgres documentation`_ explains the syntax of the config file
       that you need to change.

#. Set the environment variables for your database(s): ::

    $ export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/<DB name given to createdb>

   .. note::

       Check out the :ref:`settings` page for a comprehensive list of the environments variables.

   .. seealso::

       To help setting up your environment variables, you have a few options:

       * Create an ``.env`` file in the root of your project and define all the variables you need in it.
         Then you just need to have ``DJANGO_READ_DOT_ENV_FILE=True`` in your machine and all the variables
         will be read.
       * Use a local environment manager like `direnv`_

#. Apply migrations: ::

    $ python manage.py migrate

#. If you're running synchronously, see the application being served through Django development server: ::

    $ python manage.py runserver 0.0.0.0:8000

.. _PostgreSQL: https://www.postgresql.org/download/
.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _createdb: https://www.postgresql.org/docs/current/static/app-createdb.html
.. _initial PostgreSQL set up: https://web.archive.org/web/20190303010033/http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html
.. _postgres documentation: https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html
.. _pre-commit: https://pre-commit.com/
.. _direnv: https://direnv.net/
.. _AwsCLI: https://aws.amazon.com/cli/

Creating Your First Django App
------------------------------

After setting up your environment, you're ready to add your first app. This project uses the setup from "Two Scoops of Django" with a two-tier layout:

- **Top Level Repository Root** has config files, documentation, `manage.py`, and more.
- **Second Level Django Project Root** is where your Django apps live.
- **Second Level Configuration Root** holds settings and URL configurations.

The project layout looks something like this: ::

    <repository_root>/
    ├── config/
    │   ├── settings/
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── local.py
    │   │   └── production.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── <django_project_root>/
    │   ├── <name_of_the_app>/
    │   │   ├── migrations/
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   └── views.py
    │   ├── __init__.py
    │   └── ...
    ├── requirements/
    │   ├── base.txt
    │   ├── local.txt
    │   └── production.txt
    ├── manage.py
    ├── README.md
    └── ...

Following this structured approach, here's how to add a new app:

#. **Create the app** using Django's ``startapp`` command, replacing ``<name-of-the-app>`` with your desired app name: ::

    $ python manage.py startapp <name-of-the-app>

#. **Move the app** to the Django Project Root, maintaining the project's two-tier structure: ::

    $ mv <name-of-the-app> <django_project_root>/

#. **Edit the app's apps.py** change ``name = '<name-of-the-app>'`` to ``name = '<django_project_root>.<name-of-the-app>'``.

#. **Register the new app** by adding it to the ``LOCAL_APPS`` list in ``config/settings/base.py``, integrating it as an official component of your project.

Setup Email Backend
-------------------

To test email functionality, you can use the console backend. This backend writes emails to the console instead of sending them. To set this up, add the following to your ``config/settings/local.py``: ::

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Summary
-------

Congratulations, you should now have a working development environment set up and ready to go.

Next: :rel:`usage`