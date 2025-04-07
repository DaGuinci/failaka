from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase


class ItemssAPITestCase(TestSetupAPITestCase):

    def setUp(self):
        super().setUp()
        self.item_data = {
            'name': 'Test Item',
            'description': 'Test description',
            'author': self.hera.id,
            'type': 'Test type',
            'identification': 'Test identification',
            'site': self.site_1.uuid,
            'subItem': self.subsite_1.uuid,
            'item_date': ['2021-01-01', '2021-12-31'],
            'family': 'Test family',
            'scient_name': 'Test scientific name',
            'material': 'Test material',
            'current_location': 'Test location',
            'references': 'Test references',
            'citation': 'Test citation',
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
    def test_not_connected_cant_create_item(self):
        response = self.client.post(reverse_lazy('item-list'), self.item_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_can_list_items(self):
        response = self.client.get(reverse_lazy('item-list'))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_can_retrieve_item(self):
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        response = self.client.get(reverse_lazy('item-detail', args=[target_Item['uuid']]))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_cant_update_item(self):
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        self.item_data_update = self.item_data.copy()
        response = self.client.patch(reverse_lazy('item-detail', args=[target_Item['uuid']]), self.item_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_cant_delete_item(self):
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        response = self.client.delete(reverse_lazy('item-detail', args=[target_Item['uuid']]))
        self.assertEqual(response.status_code, 401)
    
    # connected as user
    def test_user_cant_create_item(self):
        token = self.get_token('user')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)
    
    def test_user_can_list_items(self):
        token = self.get_token('user')
        url = reverse_lazy('item-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)

    def test_user_can_retrieve_item(self):
        token = self.get_token('user')
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        response = self.client.get(reverse_lazy('item-detail', args=[target_Item['uuid']]), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_cant_update_item(self):
        token = self.get_token('user')
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        url = reverse_lazy('item-detail', args=[target_Item['uuid']])
        response = self.client.patch(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_user_cant_delete_item(self):
        token = self.get_token('user')
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        url = reverse_lazy('item-detail', args=[target_Item['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as validator    
    def test_validator_can_create_item(self):
        token = self.get_token('validator')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_validator_can_update_own_item(self):
        token = self.get_token('validator')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Item = response.data['uuid']
        url = reverse_lazy('item-detail', args=[target_Item])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def untest_validator_cant_update_other_item(self):
        token = self.get_token('validator')
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        url = reverse_lazy('item-detail', args=[target_Item['uuid']])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_validator_can_delete_own_item(self):
        token = self.get_token('validator')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Item = response.data['uuid']
        url = reverse_lazy('item-detail', args=[target_Item])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)

    def test_validator_cant_delete_item(self):
        token = self.get_token('validator')
        Items = self.client.get(reverse_lazy('item-list')).data
        target_Item = Items['results'][0]
        url = reverse_lazy('item-detail', args=[target_Item['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as admin
    def test_admin_can_create_item(self):
        token = self.get_token('admin')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_admin_can_update_own_item(self):
        token = self.get_token('admin')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Item = response.data['uuid']
        url = reverse_lazy('item-detail', args=[target_Item])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_update_other_item(self):
        token = self.get_token('validator')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Item = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('item-detail', args=[target_Item])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_delete_item(self):
        token = self.get_token('validator')
        url = reverse_lazy('item-list')
        response = self.client.post(url, self.item_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Item = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('item-detail', args=[target_Item])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)
