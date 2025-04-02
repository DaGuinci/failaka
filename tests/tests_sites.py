from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase


class SitesAPITestCase(TestSetupAPITestCase):

    def setUp(self):
        super().setUp()
        self.site_data = {
            'uuid': '1',
            'author': '',
            'name': 'Site 1',
            'type': 'Type 1',
            'description': 'Description 1',
            'keywords': ['Keyword 1', 'Keyword 2'],
            'chrono': ['2021-01-01', '2021-12-31'],
            'location': [0.0, 0.0],
            'location_name': 'Location 1',
            'geology': 'Geology 1',
            'geo_description': 'Geo Description 1',
            'historio': 'Historio 1',
            'justification': 'Justification 1'
        }
    
    def test_create_site(self):
        response = self.client.post(reverse_lazy('site-list'), self.site_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_list_sites(self):
        response = self.client.get(reverse_lazy('site-list'))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.data), 4)

    def untest_retrieve_site(self):
        response = self.client.get(reverse_lazy('site-detail', args=[self.site_data['uuid']]))
        self.assertEqual(response.status_code, 200)

    def untest_update_site(self):
        response = self.client.put(reverse_lazy('site-detail', args=[self.site_data['uuid']]), self.site_data_update, format='json')
        self.assertEqual(response.status_code, 200)

    def untest_delete_site(self):
        response = self.client.delete(reverse_lazy('site-detail', args=[self.site_data['uuid']]))
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse_lazy('site-list'))
        self.assertEqual(len(response.data), 0)
