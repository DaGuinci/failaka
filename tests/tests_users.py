import json

from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase

class UsersAPITestCase(TestSetupAPITestCase):

    def expected_reponses_content(self, test):
        if test == 'email_exists':
            return {'email': ['user with this email already exists.']}
        
        if test == 'unauthenticated':
            return {'detail': "Authentication credentials were not provided."}
        
        if test == 'invalid_email':
            return {'email': ['Enter a valid email address.']}
        
        if test == 'unauthenticated':
            return {'detail': "Authentication credentials were not provided."}
        
        if test == 'permission_denied':
            return {'detail': "You do not have permission to perform this action."}

        return None


class UserTestCases(UsersAPITestCase):

    # Get user list
    def test_non_auth_cant_get_users_list(self):
        url = reverse_lazy('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('unauthenticated'))
        
    def test_user_cant_get_users_list(self):
        url = reverse_lazy('user-list')
        self.client.force_authenticate(user=self.hades)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))
        
    def test_validator_cant_get_users_list(self):
        url = reverse_lazy('user-list')
        self.client.force_authenticate(user=self.athena)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))
    
    def test_admin_can_get_users_list(self):
        url = reverse_lazy('user-list')
        self.client.force_authenticate(user=self.hera)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 5)

    # User creation
    def test_any_can_register(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'artemis',
            'email': 'artemis@olympe.gr',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(json.loads(response.content)['email'],'artemis@olympe.gr')

    # user creation with existing email
    def test_email_exists(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'hera',
            'email': 'hera@olympe.gr',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 400)  # 400 Bad Request
        self.assertEqual(response.json(),
                        self.expected_reponses_content('email_exists'))

    # user creation with invalid email
    def test_invalid_email(self):
        url = reverse_lazy('auth_register')
        response = self.client.post(url, {
            'username': 'hera',
            'email': 'hera',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('invalid_email'))

    # user retrieval
    def test_non_auth_cant_get_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('unauthenticated'))

    def test_other_user_cant_get_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.ares)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))
    
    def test_user_can_get_self_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.hades)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'hades@olympe.gr')
    
    def test_validator_cant_get_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.athena)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))

    def test_superuser_can_get_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.zeus)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'hades@olympe.gr')

    def test_admin_can_get_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.zeus)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'hades@olympe.gr')

    # user update
    def test_non_auth_cant_update_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        response = self.client.patch(url, {
            'username': 'hades',
            'email': 'hades@gmail.com',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('unauthenticated'))
    
    def test_other_user_cant_update_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.ares)
        response = self.client.patch(url, {
            'username': 'hades',
            'email': 'hades@gmail.com',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))
        
    def test_user_can_update_self_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.hades)
        response = self.client.patch(url, {
            'username': 'hades',
            'email': 'hades@gmail.com',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'hades@gmail.com')
    
    def test_validator_cant_update_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.athena)
        response = self.client.patch(url, {
            'username': 'hades',
            'email': 'hades@gmail.com',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))
    
    def test_admin_can_update_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.hera)
        response = self.client.patch(url, {
            'username': 'hades',
            'email': 'hades@gmail.com',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'hades@gmail.com')

    def test_superuser_can_update_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.zeus)
        response = self.client.patch(url, {
            'username': 'hades',
            'email': 'hades@gmail.com',
            'password': 'password'
            }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'hades@gmail.com')
    
    def untest_user_cant_update_role(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.hades)
        response = self.client.patch(url, {
            'role': 'admin'
            }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                        {'role': ['Only admin users can change the role of an user.']})


    # user deletion
    def test_non_auth_cant_delete_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('unauthenticated'))
        
    def test_other_user_cant_delete_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.ares)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))
        
    def test_user_can_delete_self_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.hades)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    
    def test_validator_cant_delete_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.athena)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
                        self.expected_reponses_content('permission_denied'))

    def test_admin_can_delete_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.hera)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    
    def test_superuser_can_delete_user(self):
        url = reverse_lazy('user-detail', kwargs={'pk': self.hades.id, })
        self.client.force_authenticate(user=self.zeus)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_user_can_receive_token(self):
        url = reverse_lazy('auth_token')
        response = self.client.post(url, {
            'email': 'athena@olympe.gr',
            'password': 'pass'
            }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
    
    def test_user_cant_receive_token_with_wrong_password(self):
        url = reverse_lazy('auth_token')
        response = self.client.post(url, {
            'email': 'athena@olympe.gr',
            'password': 'wrong'
            }, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                        {'detail': 'No active account found with the given credentials'})
    
    