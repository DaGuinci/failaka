from rest_framework.test import APITestCase

from rest_framework.test import APIClient

from authentication.models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from entities.models import (
    Site,
    Subsite,
    Item,
    Mission,
    Notable,
    Comment
    )


# Mise en place des datas pour test

class TestSetupAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create groups
        cls.admin_group = Group.objects.create(name='admins')
        cls.validator_group = Group.objects.create(name='validators')
        cls.visitor_group = Group.objects.create(name='visitors')

        # Superuser
        UserModel = get_user_model()
        cls.zeus = UserModel.objects.create_superuser(
            email='admin@olympe.gr',
            password='pass')

        # Admin
        cls.hera = User.objects.create_user(
            # username='hera_admin',
            email='hera@olympe.gr',
            password='pass',
        )
        cls.hera.groups.set(Group.objects.filter(name='admins'))

        # Validator
        cls.athena = User.objects.create_user(
            # username='athena_validator',
            email='athena@olympe.gr',
            password='pass',
        )
        cls.athena.groups.set(Group.objects.filter(name='validators'))

        # Users
        cls.hades = User.objects.create_user(
            # username='hades_user',
            email='hades@olympe.gr',
            password='pass',
        )
        cls.hades.groups.set(Group.objects.filter(name='visitors'))

        cls.ares = User.objects.create_user(
            # username='ares_user',
            email='ares@olympe.gr',
            password='pass',
        )
        cls.ares.groups.set(Group.objects.filter(name='visitors'))

        # Sites
        cls.site_1 = Site.objects.create(
            author=cls.hera,
            name='Site 1',
            type='Type 1',
            description='Description 1',
            keywords=['Keyword 1', 'Keyword 2'],
            chrono=['2021-01-01', '2021-12-31'],
            location=[0.0, 0.0],
            location_name='Location 1',
            geology='Geology 1',
            geo_description='Geo Description 1',
            historio='Historio 1',
            justification='Justification 1'
        )

        # Subsites
        cls.subsite_1 = Subsite.objects.create(
            author=cls.hera,
            site=cls.site_1,
            name='Subsite 1',
            description='Description 1',
            chrono=['2021-01-01', '2021-12-31'],
            location=[0.0, 0.0],
            justification='Justification 1',
            settle_type='Settle Type 1',
            material='Material 1',
            remains='Remains 1'
        )

        # Items
        cls.item_1 = Item.objects.create(
            author=cls.hera,
            type='Type 1',
            identification='Identification 1',
            site=cls.site_1,
            subsite=cls.subsite_1,
            item_date=['2021-01-01', '2021-12-31'],
            family='Family 1',
            scient_name='Scient Name 1',
            material='Material 1',
            current_location='Current Location 1',
            references='References 1',
            citation='Citation 1'
        )
        cls.item_2 = Item.objects.create(
            author=cls.hera,
            type='Type 2',
            identification='Identification 2',
            site=cls.site_1,
            subsite=cls.subsite_1,
            item_date=['2021-01-01', '2021-12-31'],
            family='Family 2',
            scient_name='Scient Name 2',
            material='Material 2',
            current_location='Current Location 2',
            references='References 2',
            citation='Citation 2'
        )

        # Missions
        # - notables: Notables-manyToMany
        # - mission_members: String
        # - type: String
        # - period: String
        # - biblio: String
        # - citation: String
        cls.mission_1 = Mission.objects.create(
            author=cls.hera,
            name='Mission 1',
            description='Description 1',
            type='Type 1',
            mission_members='Members 1',
            period=['2021-01-01', '2021-12-31'],
            biblio='Biblio 1',
            citation='Citation 1'
        )

        # Notables
        cls.notable_1 = Notable.objects.create(
            author=cls.hera,
            name='Notable 1',
            description='Description 1',
            first_name='First Name 1',
            last_name='Last Name 1'
        )

        # Comments
        cls.comment_data = Comment.objects.create(
            name='Test Comment',
            description='Test description',
            author=cls.hera,
            status='pending',
            item=cls.item_1,
        )

    @classmethod
    def check_in_terminal(self, items):
        print('----------------- Comparing values -----------------')
        for item in items:
            print(item)