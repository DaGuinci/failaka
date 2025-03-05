from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase

class AuthenticationAPITestCase(TestSetupAPITestCase):

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