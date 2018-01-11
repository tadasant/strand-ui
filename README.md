# CodeClippy Portal

## Getting Started

To start, clone the repository locally and create a virtual environment. Install the dependencies
from the requirements file into your virtual environment.

### Database Configuration

To use the application, you'll need to set up a local PostgreSQL database. The following
are the bash commands to do so. Enter them into your terminal, replacing the words in CAPS
with the values you prefer.

```bash
mkdir ~/.postgres
brew install postgres
initdb -D ~/.postgres/DATABASE_NAME
pg_ctl start -D ~/.postgres/DATABASE_NAME
createdb DATABASE_NAME
createuser --superuser --createdb --createrole --login --pwprompt --encrypted USERNAME
ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
```

*Note: If you already have a Postgres server running locally on port 5432, you can create a new
database in the `psql` prompt by runinng, `CREATE DATABASE DATABASE_NAME`.*


The next step is to create a JSON config file in the config folder. It should be called `db.config.json`
and look like this:
```JSON
{
  "NAME": "DATABASE_NAME",
  "USER": "USERNAME",
  "PASSWORD": "PASSWORD",
  "HOST": "",
  "PORT": "5432"
}
```

### DB Migrations

To start the app, run `python manage.py migrate` to migrate your local database to
the latest schema.

### Create superuser

To access Django admin, you need to create a local admin user. Create a superuser by running
`python manage.py createsuperuser --username USERNAME`

