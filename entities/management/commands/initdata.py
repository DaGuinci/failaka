import json
from django.core.management import BaseCommand, call_command
from django.conf import settings
from authentication.models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with a set of data for testing purposes"

    def handle(self, *args, **options):
        # Create groups
        groups = ['admins', 'validators', 'visitors']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Group '{group_name}' created.")
            else:
                self.stdout.write(f"Group '{group_name}' already exists.")

        # Load data only in development mode
        if settings.DEBUG:
            self.stdout.write("Development mode detected. Loading fixtures...")
            call_command('loaddata', 'initial_data_users')

            # Assign groups to users based on the JSON file
            with open('entities/fixtures/initial_data_users.json', 'r') as f:
                users_data = json.load(f)

            for user_data in users_data:
                group_name = user_data.get("group")
                if group_name:
                    try:
                        user = User.objects.get(pk=user_data["pk"])
                        group = Group.objects.get(name=group_name)
                        user.groups.set([group])  # Replace existing groups
                        self.stdout.write(f"User '{user.email}' added to group '{group.name}'.")
                    except User.DoesNotExist:
                        self.stdout.write(f"User with pk '{user_data['pk']}' does not exist.")
                    except Group.DoesNotExist:
                        self.stdout.write(f"Group '{group_name}' does not exist.")

            # Fix the passwords of fixtures
            for user in User.objects.all():
                user.set_password(user.password)
                user.save()
        else:
            self.stdout.write("Production mode detected. Skipping fixture loading.")
