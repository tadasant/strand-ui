# CodeClippy Portal

[![CodeFactor](https://www.codefactor.io/repository/github/solutionloft/code-clippy-portal/badge)](https://www.codefactor.io/repository/github/solutionloft/code-clippy-portal)


## Getting Started

To start, clone the repository locally and create a virtual environment. Install the dependencies
from the requirements file into your virtual environment.

### Database Configuration

To use the application, you'll need to set up a local PostgreSQL database. The following
are the bash commands to do so. Enter them into your terminal, replacing the words in CAPS
with the values you prefer.

```bash
$ mkdir ~/.postgres
$ brew install postgres
$ initdb -D ~/.postgres/DATABASE_NAME
$ pg_ctl start -D ~/.postgres/DATABASE_NAME
$ createdb DATABASE_NAME
$ createuser --superuser --createdb --createrole --login --pwprompt --encrypted solutionloft
$ ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
```

*Note: If you already have a Postgres server running locally on port 5432, you can create a new
database in the `psql` prompt by runinng, `CREATE DATABASE DATABASE_NAME`.*


The next step is to create a JSON config file in the config folder. It should be called `db.config.json`
and look like this:
```JSON
{
  "NAME": "DATABASE_NAME",
  "USER": "solutionloft",
  "PASSWORD": "PASSWORD",
  "HOST": "",
  "PORT": "5432"
}
```

### Database Migrations

To start the app, run `$ python manage.py migrate` to migrate your local database to
the latest schema.

### Creating a Superuser

To access Django admin, you need to create a local admin user. Create a superuser by running
`$ python manage.py createsuperuser --username USERNAME`.

## Running Tests

The test suite for CodeClippy Portal uses `pytest`, `factory-boy`, `flake8`, and `pep8`. To run
tests, use the `pytest` command from the root directory. To test with `flake8` and `pep8` (which
you'll need to do before pushing to a remote branch), add them as flags to your `pytest` command.

`$ pytest --flake8 --pep8` 

## JSON Fixtures

Django uses fixtures to dump and load data for development. This allows us to build up an environment with strong mock
data that we can use during development, review, testing, etc. Fixtures are typically dumped and loaded on a 
per-app basis and can be in a variety of formats. We'll use JSON for ease-of-use.

For more on fixtures, start [here](https://docs.djangoproject.com/en/2.0/howto/initial-data/).

### Dumping data

For each app, you can dump the current database contents with the `dumpdata` command followed by the app name.
The additional flags we use are `--exclude contenttypes` to prevent integrity issues on the contenttypes tables
and `--indent 2` which simply prettifies our JSON dump.

`$ python manage.py dumpdata [APP_NAME] --exclude contenttypes --indent 2 > [APP_NAME].json`

### Loading data

Typically you load data into a different database than the one you dumped from (e.g. to a fresh local database
or to a coworker's local database). To load the data, we'll use the `loaddata` command followed by the name of the
fixture. Django looks for fixtures in the `fixtures/` directories within apps. Alternatively, you can specify
the path to the fixture, which will override this behavior.

`$ python manage.py loaddata fixture_name`

When loading fixtures, keep in mind the relationships between them. Always load them from top down, so as not to have
integrity errors. As of commit `3b73a3b`, the order is *users*, *groups*, *topics*, *slack_integration*, and
*dialogues*.

## Task Management

In the context of code-clippy-portal, we will have a number of tasks that need to run in the background, whether
they are asynchronous tasks that take longer than the expected turnaround for a query or periodic tasks
that we want to run in the background on a regular interval. To manage these tasks, we need three components: a task
queue, the beat (which adds tasks to the queue), and workers which execute tasks from the queue.

To do this, we use [Celery](http://docs.celeryproject.org/en/latest/getting-started/introduction.html#get-started),
which since version 4 has native Django support. As the queue service, we use [Redis](https://redis.io/). We also use
two Django extensions that increase the leverage we get from using Celery within Django. The first
is `django-celery-results`, which provides result backends using the Django ORM. This means rather than storing
results from jobs in Redis we can store them in Django! In Django Admin interface, the results are found under the 
*DJANGO_CELERY_RESULTS* header. The second is `django-celery-beat` which allows us to
construct periodic tasks and use the Django Admin interface to manage them. In the Django Admin interface, the
tasks are found under the *PERIODIC TASKS* header. 

### Configuring a local Redis instance

The first step is to install Redis to your computer. There are a number of ways to do so. I found the easiest to be
`$ brew install redis`. You can now set Redis to launch when your computer starts:
`$ ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents`. The last step is to launch the server: 
`$ launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist`.

To test that Redis has been installed, use the Redis CLI to ping the server: `$ redis-cli ping`.

### Starting a Celery worker

To start a Celery worker, open up another Terminal session. Using the Celery command line, you can run
`$ celery -A app worker -l info`. The `-A` flag is for specifying an app by its name, which we've done in 
`celery.py` within `app/api/`. If the project is properly configured, you should see the Celery logo along
with Redis connection information that matches that in your `local.py` file.

### Starting _the_ Beat

To start the Celery beat, open up a third Terminal session. Using the Celery command line, you can run
`$ celery -A app beat -l info`.

### Clearing out the Queue

If something goes awry, you can clear the task queue by running `$ celery -A app purge`.

### Setting up Periodic Tasks

We have two types of tasks at the moment. One is a periodic task, which runs every 5 minutes
and marks discussions as stale if there has been no non-bot activity for over 30 minutes. Another is
an asynchronous task that runs 5 minutes after a discussion has been marked as pending closed. If
there is no new activity since it was marked as pending closed, then the task closes the discussion and
the respective discussion.

The periodic task needs to exist in the `django_celery_beat` table in order for the beat to populate
it to the task queue every 5 minutes. To do this, we have a management command to create it if you haven't
already done so. To execute it, run `$ python manage create_periodic_tasks`.
