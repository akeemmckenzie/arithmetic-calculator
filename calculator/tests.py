from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Operation, Record

class UserViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

class OperationViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        Operation.objects.all().delete()  # Remove any existing operations
        self.operation = Operation.objects.create(type='addition', cost='5.00')

    def test_list_operations(self):
        url = reverse('operation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Compare actual data in the 'results' key of the paginated response
        expected_data = [
            {
                'id': self.operation.id,
                'type': self.operation.type,
                'cost': str(self.operation.cost),  # Convert the Decimal field to a string
            }
        ]
        self.assertEqual(response.data['results'], expected_data)

class RecordViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.operation = Operation.objects.create(type='addition', cost=5)
        self.record = Record.objects.create(user=self.user, operation=self.operation, amount=2, user_balance=10, operation_response='2+2=4')

    def test_soft_delete_record(self):
        url = reverse('record-detail', kwargs={'pk': self.record.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Record.objects.get(pk=self.record.pk).deleted)
