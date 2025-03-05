from rest_framework.test import APITestCase

from rest_framework.test import APIClient

from authentication.models import User

from django.contrib.auth import get_user_model


# from api.models import (
#     Project,
#     Contributing,
#     Issue,
#     Comment
#     )


# Mise en place des datas pour test

class TestSetupAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Superuser
        UserModel = get_user_model()
        cls.zeus = UserModel.objects.create_superuser('Zeus_superuser', 'admin@olympe.gr', 'pass')

        # Admin
        cls.hera = User.objects.create(
            username='hera_admin',
            email='hera@olympe.gr',
            password='pass',
            role='admin'
        )

        # validator
        cls.athena = User.objects.create(
            username='athena_validator',
            email='athena@olympe.gr',
            password='pass',
            role='validator'
        )

        # User
        cls.hades = User.objects.create(
            username='hades_user',
            email='hades@olympe.gr',
            password='pass',
            role='user'
        )

        cls.ares = User.objects.create(
            username='ares_user',
            email='ares@olympe.gr',
            password='pass',
            role='user'
        )

    @classmethod
    def check_in_terminal(self, items):
        print('----------------- Comparing values -----------------')
        for item in items:
            print(item)