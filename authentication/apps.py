import os
from django.apps import AppConfig
from django.core.management import call_command

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    # Réinitialise et recharge les données
    def ready(self):
        print('DJANGO_ENV:', os.environ.get('DJANGO_ENV'))
        if os.environ.get('DJANGO_ENV') == 'development':
            call_command('flush', '--no-input')
            call_command('migrate')
            call_command('loaddata', 'authentication/data_init.json')