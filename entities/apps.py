import os
from django.apps import AppConfig
from django.core.management import call_command

class EntitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entities'
