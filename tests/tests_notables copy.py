from django.urls import reverse_lazy

from .tests_data_setup import TestSetupAPITestCase

class CommentAPITestCase(TestSetupAPITestCase):

    def setUp(self):
        super().setUp()
        self.comment_data = {
            'name': 'Test Comment',
            'description': 'Test description',
            'author': self.hera.id,
            'status': 'pending',
            'item': self.item_1.id,
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
    def test_not_connected_cant_create_comment(self):
        response = self.client.post(reverse_lazy('comment-list'), self.comment_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_can_list_comments(self):
        response = self.client.get(reverse_lazy('comment-list'))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_can_retrieve_comment(self):
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        response = self.client.get(reverse_lazy('comment-detail', args=[target_Comment['uuid']]))
        self.assertEqual(response.status_code, 200)

    def test_not_connected_cant_update_comment(self):
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        self.comment_data_update = self.comment_data.copy()
        response = self.client.patch(reverse_lazy('comment-detail', args=[target_Comment['uuid']]), self.comment_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_connected_cant_delete_comment(self):
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        response = self.client.delete(reverse_lazy('comment-detail', args=[target_Comment['uuid']]))
        self.assertEqual(response.status_code, 401)
    
    # connected as user
    def test_user_cant_create_comment(self):
        token = self.get_token('user')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)
    
    def test_user_can_list_comments(self):
        token = self.get_token('user')
        url = reverse_lazy('comment-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)

    def test_user_can_retrieve_comment(self):
        token = self.get_token('user')
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        response = self.client.get(reverse_lazy('comment-detail', args=[target_Comment['uuid']]), HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_cant_update_comment(self):
        token = self.get_token('user')
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        url = reverse_lazy('comment-detail', args=[target_Comment['uuid']])
        response = self.client.patch(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_user_cant_delete_comment(self):
        token = self.get_token('user')
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        url = reverse_lazy('comment-detail', args=[target_Comment['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as validator    
    def test_validator_can_create_comment(self):
        token = self.get_token('validator')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_validator_can_update_own_comment(self):
        token = self.get_token('validator')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Comment = response.data['uuid']
        url = reverse_lazy('comment-detail', args=[target_Comment])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def untest_validator_cant_update_other_comment(self):
        token = self.get_token('validator')
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        url = reverse_lazy('comment-detail', args=[target_Comment['uuid']])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    def test_validator_can_delete_own_comment(self):
        token = self.get_token('validator')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Comment = response.data['uuid']
        url = reverse_lazy('comment-detail', args=[target_Comment])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)

    def test_validator_cant_delete_comment(self):
        token = self.get_token('validator')
        Comment = self.client.get(reverse_lazy('comment-list')).data
        target_Comment = Comment['results'][0]
        url = reverse_lazy('comment-detail', args=[target_Comment['uuid']])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 403)

    # connected as admin
    def test_admin_can_create_comment(self):
        token = self.get_token('admin')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 201)

    def test_admin_can_update_own_comment(self):
        token = self.get_token('admin')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Comment = response.data['uuid']
        url = reverse_lazy('comment-detail', args=[target_Comment])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_update_other_comment(self):
        token = self.get_token('validator')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Comment = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('comment-detail', args=[target_Comment])
        response = self.client.patch(url, {'name': 'other name'}, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'other name')

    def test_admin_can_delete_comment(self):
        token = self.get_token('validator')
        url = reverse_lazy('comment-list')
        response = self.client.post(url, self.comment_data, format='json', HTTP_AUTHORIZATION=f'Bearer {token}')
        target_Comment = response.data['uuid']
        token = self.get_token('admin')
        url = reverse_lazy('comment-detail', args=[target_Comment])
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 204)
