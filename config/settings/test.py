import os
import json

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
SLACK_CLIENT_ID = '000000000000.111111111111'
SLACK_CLIENT_SECRET = '1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a'
SLACK_VERIFICATION_TOKEN = '123ABC123ABC123ABC123ABC'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'

# Session Auto-Close Delay
AUTO_CLOSE_DELAY = 4
