from django.core.management import BaseCommand, call_command
from django.conf import settings
from authentication.models import User
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with a set of data for testing purposes"

    def handle(self, *args, **options):
        # Create groups
        groups_permissions = {
            'admins': ['add_user', 'change_user', 'delete_user', 'view_user'],
            'validators': ['can_validate'],
            'visitors': ['view_user'],
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Group '{group_name}' created.")
            else:
                self.stdout.write(f"Group '{group_name}' already exists.")

            # Assign permissions to the group
            for perm_codename in permissions:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(f"Permission '{perm_codename}' does not exist.")

        # Load data only in development mode
        if settings.DEBUG:
            self.stdout.write("Development mode detected. Loading fixtures...")
            call_command('loaddata', 'initial_data_users')
            call_command('loaddata', 'initial_data_missions')
            call_command('loaddata', 'initial_data_sites')
            # call_command('loaddata', 'initial_data_items')
            # call_command('loaddata', 'initial_data_others')

            # Fix the passwords of fixtures
            for user in User.objects.all():
                user.set_password(user.password)
                user.save()
        else:
            self.stdout.write("Production mode detected. Skipping fixture loading.")
