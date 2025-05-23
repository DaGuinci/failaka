from django.core.management import BaseCommand, call_command
# from django.contrib.auth.models import User
from authentication.models import User # if you have a custom user


class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data_users')
        call_command('loaddata', 'initial_data_sites')
        call_command('loaddata', 'initial_data_items')
        call_command('loaddata', 'initial_data_others')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
