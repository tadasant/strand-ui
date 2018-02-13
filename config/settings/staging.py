import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT']
    }
}

ENABLE_GRAPHIQL = True
CSRF_COOKIE_SECURE = True

# Slack credentials
SLACK_CLIENT_ID = os.environ['SLACK_CLIENT_ID']
SLACK_CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']
SLACK_VERIFICATION_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']

# Celery
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

# Discussion Auto-Close Delay
AUTO_CLOSE_DELAY = 300

# Slack App Verification Token
SLACK_APP_VERIFICATION_TOKEN = os.environ['SLACK_APP_VERIFICATION_TOKEN']
SLACK_APP_STALE_DISCUSSION_ENDPOINT = os.environ['SLACK_APP_STALE_DISCUSSIONS_ENDPOINT']
SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT = os.environ['SLACK_APP_AUTO_CLOSED_DISCUSSIONS_ENDPOINT']
