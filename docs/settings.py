# docs/settings.py

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'frame',  # Add your app here
]

# Minimal settings required
SECRET_KEY = 'dummy-key'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Define the user model if your app depends on a custom user model
AUTH_USER_MODEL = 'auth.User'

AWS_REGION = 'us-west-2'