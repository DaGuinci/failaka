from django.core.management.base import BaseCommand
from entities.models import Site
from entities.serializers import SiteSerializer
from authentication.models import User

# Unused function: commented in apps.py
class Command(BaseCommand):
    help = 'Create initial entities'

    def handle(self, *args, **kwargs):
        # sites creation
        # get author user by email
        author = User.objects.get(email='admin@failalka.com').id
        sites = [
            # Site 1
            {
                'author': author,
                'name': 'Site 1',
                'type': 'Type 1',
                'description': 'Description 1',
                'keywords': ['Keyword 1', 'Keyword 2'],
                'chrono': ['2021-01-01', '2021-12-31'],
                'location': [0.0, 0.0],
                'location_name': 'Location 1',
                'geology': 'Geology 1',
                'geo_description': 'Geo Description 1',
                'historio': 'Historio 1',
                'justification': 'Justification 1'
            },
        ]

        for site_data in sites:
            if not Site.objects.filter(name=site_data['name']).exists():
                serializer = SiteSerializer(data=site_data)
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS(f"site {site_data['name']} created successfully"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error creating site {site_data['name']}: {serializer.errors}"))
            else:
                self.stdout.write(self.style.WARNING(f"site {site_data['name']} already exists"))