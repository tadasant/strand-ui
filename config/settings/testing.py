import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'solutionloft',
        'USER': 'solutionloft',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

ENABLE_GRAPHIQL = False
CSRF_COOKIE_SECURE = False

# Slack credentials
SLACK_CLIENT_SECRET = '1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'

# Discussion Auto-Close Delay
AUTO_CLOSE_DELAY = 4

SLACK_APP_VERIFICATION_TOKEN = 'anoTH3rRANDoMCOmbo'
SLACK_APP_STALE_DISCUSSION_ENDPOINT = 'http://slackapp.com/stalediscussions'
SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT = 'http://slackapp.com/autocloseddiscussions'
SLACK_APP_SLACK_AGENT_ENDPOINT = 'http://slackapp.com/slackagents'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
