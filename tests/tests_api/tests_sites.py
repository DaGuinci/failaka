from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase


class SitesAPITestCase(TestSetupAPITestCase):

    def setUp(self):
        super().setUp()
        self.site_data = {
            'name': 'Site 1',
            'description': 'Description 1',
            'type': 'Type 1',
            'keywords': ['Keyword 1', 'Keyword 2'],
            'chrono': ['2021-01-01', '2021-12-31'],
            'location': [0.0, 0.0],
            'location_name': 'Location 1',
            'geology': 'Geology 1',
            'geo_description': 'Geo Description 1',
            'historio': 'Historio 1',
            'justification': 'Justification 1'
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
    def test_not_connected_cant_create_site(self):
        response = self.client.post(reverse_lazy('site-list'), self.site_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_can_list_sites(self):
        response = self.client.get(reverse_lazy('site-list'))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_can_retrieve_site(self):
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        response = self.client.get(reverse_lazy('site-detail', args=[target_site['uuid']]))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_cant_update_site(self):
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        self.site_data_update = self.site_data.copy()
        response = self.client.patch(reverse_lazy('site-detail', args=[target_site['uuid']]), self.site_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_cant_delete_site(self):
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        response = self.client.delete(reverse_lazy('site-detail', args=[target_site['uuid']]))
        self.assertEqual(response.status_code, 401)
    
    # connected as user
    def test_user_cant_create_site(self):
        token = self.get_token('user')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)
    
    def test_user_can_list_sites(self):
        token = self.get_token('user')
        url = reverse_lazy('site-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)

    def test_user_can_retrieve_site(self):
        token = self.get_token('user')
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        response = self.client.get(reverse_lazy('site-detail', args=[target_site['uuid']]), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_cant_update_site(self):
        token = self.get_token('user')
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        url = reverse_lazy('site-detail', args=[target_site['uuid']])
        response = self.client.patch(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_user_cant_delete_site(self):
        token = self.get_token('user')
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        url = reverse_lazy('site-detail', args=[target_site['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as validator    
    def test_validator_can_create_site(self):
        token = self.get_token('validator')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_validator_can_update_own_site(self):
        token = self.get_token('validator')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_site = response.data['uuid']
        url = reverse_lazy('site-detail', args=[target_site])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def untest_validator_cant_update_other_site(self):
        token = self.get_token('validator')
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        url = reverse_lazy('site-detail', args=[target_site['uuid']])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_validator_can_delete_own_site(self):
        token = self.get_token('validator')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_site = response.data['uuid']
        url = reverse_lazy('site-detail', args=[target_site])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)

    def test_validator_cant_delete_site(self):
        token = self.get_token('validator')
        sites = self.client.get(reverse_lazy('site-list')).data
        target_site = sites['results'][0]
        url = reverse_lazy('site-detail', args=[target_site['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as admin
    def test_admin_can_create_site(self):
        token = self.get_token('admin')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_admin_can_update_own_site(self):
        token = self.get_token('admin')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_site = response.data['uuid']
        url = reverse_lazy('site-detail', args=[target_site])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_update_other_site(self):
        token = self.get_token('validator')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_site = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('site-detail', args=[target_site])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_delete_site(self):
        token = self.get_token('validator')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_site = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('site-detail', args=[target_site])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)
