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
        else:
            return None
    
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
    
    def test_admin_can_create_site(self):
        token = self.get_token('admin')
        url = reverse_lazy('site-list')
        response = self.client.post(url, self.site_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        print(response.json())
        self.assertEqual(response.status_code, 201)

    def untest_update_site(self):
        response = self.client.put(reverse_lazy('site-detail', args=[self.site_data['uuid']]), self.site_data_update, format='json')
        self.assertEqual(response.status_code, 200)

    def untest_delete_site(self):
        response = self.client.delete(reverse_lazy('site-detail', args=[self.site_data['uuid']]))
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse_lazy('site-list'))
        self.assertEqual(len(response.data), 0)
