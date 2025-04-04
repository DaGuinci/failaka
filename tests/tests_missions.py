from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase


class MissionssAPITestCase(TestSetupAPITestCase):

    def setUp(self):
        super().setUp()
        self.mission_data = {
            # - notables: Notables-manyToMany
            # - mission_members: String
            # - type: String
            # - period: String
            # - biblio: String
            # - citation: String
            'name': 'Test Mission',
            'description': 'Test description',
            'author': self.hera.id,
            'type': 'Test type',
            'mission_members': 'Test members',
            'period': '2021-01-01 2021-12-31',
            'biblio': 'Test biblio',
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
    def test_not_connected_cant_create_mission(self):
        response = self.client.post(reverse_lazy('mission-list'), self.mission_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_can_list_missions(self):
        response = self.client.get(reverse_lazy('mission-list'))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_can_retrieve_mission(self):
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        response = self.client.get(reverse_lazy('mission-detail', args=[target_Mission['uuid']]))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_cant_update_mission(self):
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        self.mission_data_update = self.mission_data.copy()
        response = self.client.patch(reverse_lazy('mission-detail', args=[target_Mission['uuid']]), self.mission_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_cant_delete_mission(self):
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        response = self.client.delete(reverse_lazy('mission-detail', args=[target_Mission['uuid']]))
        self.assertEqual(response.status_code, 401)
    
    # connected as user
    def test_user_cant_create_mission(self):
        token = self.get_token('user')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)
    
    def test_user_can_list_missions(self):
        token = self.get_token('user')
        url = reverse_lazy('mission-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)

    def test_user_can_retrieve_mission(self):
        token = self.get_token('user')
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        response = self.client.get(reverse_lazy('mission-detail', args=[target_Mission['uuid']]), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_cant_update_mission(self):
        token = self.get_token('user')
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        url = reverse_lazy('mission-detail', args=[target_Mission['uuid']])
        response = self.client.patch(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_user_cant_delete_mission(self):
        token = self.get_token('user')
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        url = reverse_lazy('mission-detail', args=[target_Mission['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as validator    
    def test_validator_can_create_mission(self):
        token = self.get_token('validator')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_validator_can_update_own_mission(self):
        token = self.get_token('validator')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Mission = response.data['uuid']
        url = reverse_lazy('mission-detail', args=[target_Mission])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def untest_validator_cant_update_other_mission(self):
        token = self.get_token('validator')
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        url = reverse_lazy('mission-detail', args=[target_Mission['uuid']])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_validator_can_delete_own_mission(self):
        token = self.get_token('validator')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Mission = response.data['uuid']
        url = reverse_lazy('mission-detail', args=[target_Mission])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)

    def test_validator_cant_delete_mission(self):
        token = self.get_token('validator')
        Missions = self.client.get(reverse_lazy('mission-list')).data
        target_Mission = Missions['results'][0]
        url = reverse_lazy('mission-detail', args=[target_Mission['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as admin
    def test_admin_can_create_mission(self):
        token = self.get_token('admin')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_admin_can_update_own_mission(self):
        token = self.get_token('admin')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Mission = response.data['uuid']
        url = reverse_lazy('mission-detail', args=[target_Mission])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_update_other_mission(self):
        token = self.get_token('validator')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Mission = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('mission-detail', args=[target_Mission])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_delete_mission(self):
        token = self.get_token('validator')
        url = reverse_lazy('mission-list')
        response = self.client.post(url, self.mission_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Mission = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('mission-detail', args=[target_Mission])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)
