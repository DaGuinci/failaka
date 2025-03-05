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

        # # Nomination d'un contributeur
        # cls.contributing = Contributing.objects.create(
        #     contributor=cls.ulysse,
        #     project=cls.project_1
        # )

        # # Creation d'un issue
        # cls.issue_1 = Issue.objects.create(
        #     author=cls.ulysse,
        #     title='Artemis semble em colère',
        #     description='Agamemnon l\'a provoquée',
        #     status='TD',
        #     priority='MD',
        #     assigned_to=cls.achille,
        #     tag='TAS',
        #     project=cls.project_1
        # )

        # # Creation d'un comment
        # cls.comment_1 = Comment.objects.create(
        #     author=cls.achille,
        #     description='Des nouvelles de Patrocle ?',
        #     issue=cls.issue_1,
        # )

    @classmethod
    def check_in_terminal(self, items):
        print('----------------- Comparing values -----------------')
        for item in items:
            print(item)