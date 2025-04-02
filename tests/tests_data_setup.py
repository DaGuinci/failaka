from rest_framework.test import APITestCase

from rest_framework.test import APIClient

from authentication.models import User

from django.contrib.auth import get_user_model

from entities.models import Site


# Mise en place des datas pour test

class TestSetupAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Superuser
        UserModel = get_user_model()
        cls.zeus = UserModel.objects.create_superuser('Zeus_superuser', 'admin@olympe.gr', 'pass')

        # Admin
        cls.hera = User.objects.create_user(
            username='hera_admin',
            email='hera@olympe.gr',
            password='pass',
            role='admin'
        )

        # validator
        cls.athena = User.objects.create_user(
            username='athena_validator',
            email='athena@olympe.gr',
            password='pass',
            role='validator'
        )

        # Users
        cls.hades = User.objects.create_user(
            username='hades_user',
            email='hades@olympe.gr',
            password='pass',
        )

        cls.ares = User.objects.create_user(
            username='ares_user',
            email='ares@olympe.gr',
            password='pass',
        )

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

    @classmethod
    def check_in_terminal(self, items):
        print('----------------- Comparing values -----------------')
        for item in items:
            print(item)