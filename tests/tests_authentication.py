import json

from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase

class AuthAPITestCase(TestSetupAPITestCase):

    def expected_reponses_content(self, test):
        if test == 'email_exists':
            return {'email': ['user with this email already exists.']}
        if test == 'username_exists':
            return {'username': ['Cet utilisateur existe déjà.']}
        
        if test == 'unauthenticated':
            return {'detail': "Informations d'authentification non fournies."}
        # if test == 'modified_profile':
        #     return {
        #         'username': 'hector',
        #         'age': 27,
        #         'can_be_contacted': True,
        #         'can_data_be_shared': False
        #         }
        return None


class UserTestCases(AuthAPITestCase):

    # Get user list
    def test_can_get_users_list(self):
        url = reverse_lazy('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['username'], 'Zeus_superuser')

    # User creation
    def test_any_can_register(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'artemis',
            'email': 'artemis@olympe.gr',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(json.loads(response.content)['username'],'artemis')

    # user creation with existing email
    def untest_email_exists(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'hera',
            'email': 'artemis@olympe.gr',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 400)  # 400 Bad Request
        self.assertEqual(response.json(),
                         self.expected_reponses_content('email_exists'))



    # # Création d'un utilisateur trop jeune
    # def test_is_too_young(self):
    #     url = reverse_lazy('auth_register')
    #     response = self.client.post(url, {
    #         'username': 'agamemnon',
    #         'password': 'pass',
    #         'age': 14,
    #         'can_be_contacted': True,
    #         'can_data_be_shared': False
    #         }, format='json')
    #     self.assertEqual(response.status_code, 400)  # 400 Bad Request
    #     self.assertEqual(response.json(),
    #                      self.expected_reponses_content('is_too_young'))

    # Visualisation et modification de profil utilisateur
    # def test_can_view_profile(self):
    #     url = reverse_lazy('user-detail', kwargs={'pk': self.hector.id, })

    #     # depuis user non authentifié
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 401)  # 401 Unauthorized

    #     # depuis autre user non authentifié
    #     self.client.force_authenticate(user=self.achille)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 403)  # 403 Forbidden

    #     # depuis user sur son profil
    #     self.client.force_authenticate(user=self.hector)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)  # 200 OK

    #     # superuser
    #     self.client.force_authenticate(user=self.zeus)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)  # 200 OK

    # test des update
    # def test_can_update_profile(self):
    #     post_data = {
    #         'username': 'hector',
    #         'password': 'passwordTest',
    #         'age': 27,
    #         'can_be_contacted': True,
    #         'can_data_be_shared': False
    #         }
    #     url = reverse_lazy('user-detail', kwargs={'pk': self.hector.id, })

    #     # test methode post
    #     response = self.client.post(url, post_data, format='json')
    #     self.assertEqual(response.status_code, 401)  # 401 Unauthorized

    #     # sans authentification
    #     response = self.client.patch(url, post_data, format='json')
    #     self.assertEqual(response.status_code, 401)

    #     # depuis autre user
    #     self.client.force_authenticate(user=self.achille)
    #     response = self.client.patch(url, post_data, format='json')
    #     self.assertEqual(response.status_code, 403)

    #     # depuis user lui-même
    #     self.client.force_authenticate(user=self.hector)
    #     response = self.client.patch(url, post_data, format='json')
    #     response.json().pop('id')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(),
    #                      self.expected_reponses_content('modified_profile'))

    # test de suppression
    # def test_can_delete_profile(self):
    #     url = reverse_lazy('user-detail', kwargs={'pk': self.hector.id, })

    #     # user non authentifié
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 401)

    #     # autre user
    #     self.client.force_authenticate(user=self.achille)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 403)

    #     # lui même
    #     self.client.force_authenticate(user=self.hector)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 204)  # 204 Ok, No Content
    #     # l'user est il bien supprimé ?
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 404)  # 404 Not Found

    # test de l'appel de liste d'users
    # def test_can_get_users_list(self):
    #     url = reverse_lazy('user-list')

    #     # user non authentifié
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 401)  # 401 Unauthorized

    #     # user authentifié
    #     self.client.force_authenticate(user=self.achille)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 403)

    #     # Superuser
    #     self.client.force_authenticate(user=self.zeus)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)