import os
from django.apps import AppConfig
from django.core.management import call_command


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    # Drop and recreate the database:
    def ready(self):
        if os.environ.get('DJANGO_ENV') == 'development':
            from django.contrib.auth.models import User
            call_command('flush', '--no-input')
            call_command('migrate')
            call_command('create_users')
            # call_command('createsuperuser', '--noinput')