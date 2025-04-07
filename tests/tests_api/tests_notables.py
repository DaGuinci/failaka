from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase


class NotablessAPITestCase(TestSetupAPITestCase):

    def setUp(self):
        super().setUp()
        self.notable_data = {
            'name': 'Test Notable',
            'description': 'Test description',
            'author': self.hera.id,
            'first_name': 'Test first name',
            'last_name': 'Test last name',
            }

    def get_token(self, role):
        if role == 'admin':
            url = reverse_lazy('auth_token')
            response = self.client.post(url, {
                'email': 'hera@olympe.gr',
                'password': 'pass'
            }, format='json')
            return response.json()['access']
        elif role == 'validator':
            url = reverse_lazy('auth_token')
            response = self.client.post(url, {
                'email': 'athena@olympe.gr',
                'password': 'pass'
            }, format='json')
            return response.json()['access']
        elif role == 'user':
            url = reverse_lazy('auth_token')
            response = self.client.post(url, {
                'email': 'hades@olympe.gr',
                'password': 'pass'
            }, format='json')
            return response.json()['access']

        else:
            return None
    
    # not connected
    def test_not_connected_cant_create_notable(self):
        response = self.client.post(reverse_lazy('notable-list'), self.notable_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_can_list_notables(self):
        response = self.client.get(reverse_lazy('notable-list'))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_can_retrieve_notable(self):
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        response = self.client.get(reverse_lazy('notable-detail', args=[target_Notable['uuid']]))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_cant_update_notable(self):
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        self.notable_data_update = self.notable_data.copy()
        response = self.client.patch(reverse_lazy('notable-detail', args=[target_Notable['uuid']]), self.notable_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_cant_delete_notable(self):
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        response = self.client.delete(reverse_lazy('notable-detail', args=[target_Notable['uuid']]))
        self.assertEqual(response.status_code, 401)
    
    # connected as user
    def test_user_cant_create_notable(self):
        token = self.get_token('user')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)
    
    def test_user_can_list_notables(self):
        token = self.get_token('user')
        url = reverse_lazy('notable-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)

    def test_user_can_retrieve_notable(self):
        token = self.get_token('user')
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        response = self.client.get(reverse_lazy('notable-detail', args=[target_Notable['uuid']]), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_cant_update_notable(self):
        token = self.get_token('user')
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        url = reverse_lazy('notable-detail', args=[target_Notable['uuid']])
        response = self.client.patch(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_user_cant_delete_notable(self):
        token = self.get_token('user')
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        url = reverse_lazy('notable-detail', args=[target_Notable['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as validator    
    def test_validator_can_create_notable(self):
        token = self.get_token('validator')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_validator_can_update_own_notable(self):
        token = self.get_token('validator')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Notable = response.data['uuid']
        url = reverse_lazy('notable-detail', args=[target_Notable])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def untest_validator_cant_update_other_notable(self):
        token = self.get_token('validator')
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        url = reverse_lazy('notable-detail', args=[target_Notable['uuid']])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_validator_can_delete_own_notable(self):
        token = self.get_token('validator')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Notable = response.data['uuid']
        url = reverse_lazy('notable-detail', args=[target_Notable])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)

    def test_validator_cant_delete_notable(self):
        token = self.get_token('validator')
        Notables = self.client.get(reverse_lazy('notable-list')).data
        target_Notable = Notables['results'][0]
        url = reverse_lazy('notable-detail', args=[target_Notable['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as admin
    def test_admin_can_create_notable(self):
        token = self.get_token('admin')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_admin_can_update_own_notable(self):
        token = self.get_token('admin')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Notable = response.data['uuid']
        url = reverse_lazy('notable-detail', args=[target_Notable])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_update_other_notable(self):
        token = self.get_token('validator')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Notable = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('notable-detail', args=[target_Notable])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_delete_notable(self):
        token = self.get_token('validator')
        url = reverse_lazy('notable-list')
        response = self.client.post(url, self.notable_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Notable = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('notable-detail', args=[target_Notable])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)
