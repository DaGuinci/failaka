from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = 'Create initial users with encrypted passwords'

    def handle(self, *args, **kwargs):
        users = [
            {'username': 'admin', 'email': 'admin@myproject.com', 'password': 'password', 'is_superuser': True, 'is_staff': True},
            # Ajoutez d'autres utilisateurs ici si nécessaire
        ]

        for user_data in users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    is_superuser=user_data['is_superuser'],
                    is_staff=user_data['is_staff']
                )
                self.stdout.write(self.style.SUCCESS(f"User {user_data['username']} created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))