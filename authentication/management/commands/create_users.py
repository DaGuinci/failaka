from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = 'Create initial users with encrypted passwords'

    def handle(self, *args, **kwargs):
        users = [
            # SuperAdministrator
            {
                'email': 'superadmin@myproject.com',
                'password': 'password',
                'role': 'admin',
                'is_superuser': True,
                'is_staff': True
            },
            # Administrateur
            {
                'email': 'admin@failalka.com',
                'password': 'password',
                'role': 'admin',
                'is_superuser': False,
                'is_staff': False
            },
            # Validator
            {
                'email': 'validator@failalka.com',
                'password': 'password',
                'role': 'validator',
                'is_superuser': False,
                'is_staff': False
            },
            # Visiteur
            {
                'email': 'visitor@failalka.com',
                'password': 'password',
                'role': 'visitor',
                'is_superuser': False,
                'is_staff': False
            },
        ]

        for user_data in users:
            if not User.objects.filter(email=user_data['email']).exists():
                User.objects.create_user(
                    username=user_data['email'],
                    email=user_data['email'],
                    password=user_data['password'],
                    is_superuser=user_data['is_superuser'],
                    is_staff=user_data['is_staff'],
                    role=user_data['role']
                )
                self.stdout.write(self.style.SUCCESS(f"User {user_data['email']} created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['email']} already exists"))