import os

# Prevent HTTP Host header attacks
# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['portal-production.us-east-1.elasticbeanstalk.com', 'api.trystrand.com']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

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

ENABLE_GRAPHIQL = False

# SSL/HTTPS
# https://docs.djangoproject.com/en/2.0/topics/security/
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

# Slack credentials
SLACK_CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']

# Celery
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

# Discussion Auto-Close Delay
AUTO_CLOSE_DELAY = 300

# Slack App Verification Token
SLACK_APP_VERIFICATION_TOKEN = os.environ['SLACK_APP_VERIFICATION_TOKEN']
SLACK_APP_STALE_DISCUSSION_ENDPOINT = os.environ['SLACK_APP_STALE_DISCUSSION_ENDPOINT']
SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT = os.environ['SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT']
SLACK_APP_SLACK_AGENT_ENDPOINT = os.environ['SLACK_APP_SLACK_AGENT_ENDPOINT']

# django-storages
# http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
