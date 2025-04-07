from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase


class SubsitesAPITestCase(TestSetupAPITestCase):

    def setUp(self):
        super().setUp()
        self.subsite_data = {
            'name': 'Subsite 1',
            'description': 'Description 1',
            'site': self.site_1.uuid,
            'type': 'Type 1',
            'chrono': ['2021-01-01', '2021-12-31'],
            'location': [0.0, 0.0],
            'justification': 'Justification 1',
            'settle_type': 'Settle Type 1',
            'material': 'Material 1',
            'remains': 'Remains 1'
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
    def test_not_connected_cant_create_subsite(self):
        response = self.client.post(reverse_lazy('subsite-list'), self.subsite_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_can_list_subsites(self):
        response = self.client.get(reverse_lazy('subsite-list'))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_can_retrieve_subsite(self):
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        response = self.client.get(reverse_lazy('subsite-detail', args=[target_subsite['uuid']]))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_cant_update_subsite(self):
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        self.subsite_data_update = self.subsite_data.copy()
        response = self.client.patch(reverse_lazy('subsite-detail', args=[target_subsite['uuid']]), self.subsite_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_cant_delete_subsite(self):
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        response = self.client.delete(reverse_lazy('subsite-detail', args=[target_subsite['uuid']]))
        self.assertEqual(response.status_code, 401)
    
    # connected as user
    def test_user_cant_create_subsite(self):
        token = self.get_token('user')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)
    
    def test_user_can_list_subsites(self):
        token = self.get_token('user')
        url = reverse_lazy('subsite-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)

    def test_user_can_retrieve_subsite(self):
        token = self.get_token('user')
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        response = self.client.get(reverse_lazy('subsite-detail', args=[target_subsite['uuid']]), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_cant_update_subsite(self):
        token = self.get_token('user')
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        url = reverse_lazy('subsite-detail', args=[target_subsite['uuid']])
        response = self.client.patch(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_user_cant_delete_subsite(self):
        token = self.get_token('user')
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        url = reverse_lazy('subsite-detail', args=[target_subsite['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as validator    
    def test_validator_can_create_subsite(self):
        token = self.get_token('validator')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_validator_can_update_own_subsite(self):
        token = self.get_token('validator')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_subsite = response.data['uuid']
        url = reverse_lazy('subsite-detail', args=[target_subsite])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def untest_validator_cant_update_other_subsite(self):
        token = self.get_token('validator')
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        url = reverse_lazy('subsite-detail', args=[target_subsite['uuid']])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_validator_can_delete_own_subsite(self):
        token = self.get_token('validator')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_subsite = response.data['uuid']
        url = reverse_lazy('subsite-detail', args=[target_subsite])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)

    def test_validator_cant_delete_subsite(self):
        token = self.get_token('validator')
        subsites = self.client.get(reverse_lazy('subsite-list')).data
        target_subsite = subsites['results'][0]
        url = reverse_lazy('subsite-detail', args=[target_subsite['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as admin
    def test_admin_can_create_subsite(self):
        token = self.get_token('admin')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_admin_can_update_own_subsite(self):
        token = self.get_token('admin')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_subsite = response.data['uuid']
        url = reverse_lazy('subsite-detail', args=[target_subsite])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_update_other_subsite(self):
        token = self.get_token('validator')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_subsite = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('subsite-detail', args=[target_subsite])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_delete_subsite(self):
        token = self.get_token('validator')
        url = reverse_lazy('subsite-list')
        response = self.client.post(url, self.subsite_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_subsite = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('subsite-detail', args=[target_subsite])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)
