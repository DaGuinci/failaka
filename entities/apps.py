import os
from django.apps import AppConfig
from django.core.management import call_command

class EntitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entities'

    # create instances of the models:
    def ready(self):
        if os.environ.get('DJANGO_ENV') == 'development':
            from entities.models import Site
            call_command('create_entities')