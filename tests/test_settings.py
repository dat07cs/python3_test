from python_test.settings import *

SECRET_KEY = 'fake-key'

BASE_URL = 'http://testserver/'
ALLOWED_HOSTS = ['testserver']

INSTALLED_APPS = (
    'tests',
    'rest_framework',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tests/test_database.sqlite3',
    },
    'slave': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tests/test_database.sqlite3',
        'TEST': {
            'MIRROR': 'default',
        }
    },
}

TEST_RUNNER = 'tests.test_runner.FastTestRunner'

LOGGING['handlers']['console'] = {'class': 'logging.StreamHandler', 'level': 'WARNING'}
for logger in LOGGING['loggers'].keys():
    LOGGING['loggers'][logger]['handlers'] = ['console']
    LOGGING['loggers'][logger]['level'] = 'INFO'
