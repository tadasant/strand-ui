import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DB_CREDENTIALS = json.load(open(os.path.join(BASE_DIR, 'db.config.json'), 'r'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_CREDENTIALS['NAME'],
        'USER': DB_CREDENTIALS['USER'],
        'PASSWORD': DB_CREDENTIALS['PASSWORD'],
        'HOST': DB_CREDENTIALS['HOST'],
        'PORT': DB_CREDENTIALS['PORT']
    }
}

ENABLE_GRAPHIQL = True
CSRF_COOKIE_SECURE = False

# Slack credentials
SLACK_CLIENT_ID = '299839214388.299854203762'
SLACK_CLIENT_SECRET = '6d9bb9189b347be559ee46159025b96c'
SLACK_VERIFICATION_TOKEN = 'wRto4JPoZXVH2ru3HHJ4nBRL'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'

# Discussion Auto-Close Delay
AUTO_CLOSE_DELAY = 300

SLACK_APP_VERIFICATION_TOKEN = 'anoTH3rRANDoMCOmbo'
SLACK_APP_STALE_DISCUSSION_ENDPOINT = 'http://slackapp.com/stalediscussions'
SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT = 'http://slackapp.com/autocloseddiscussions'
SLACK_APP_SLACK_AGENT_ENDPOINT = 'http://slackapp.com/slackagents'

