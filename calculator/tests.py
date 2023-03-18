from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Operation, Record
import json
from .utils import get_random_string
from rest_framework.test import force_authenticate, APIRequestFactory

class AdditionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.operation = Operation.objects.create(type='addition', cost=1.0)
        self.url = reverse('addition')

    def test_addition(self):
        self.client.force_authenticate(user=self.user)  # Add authentication to the request
        data = {'value1': 1, 'value2': 2}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'result': '3.0'})

class MultiplicationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operation = Operation.objects.create(type='multiplication', cost=2)
        self.url = reverse('multiplication')

    def test_multiplication(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass')
        user.credit = 100  # set initial credit to 100
        user.save()

        data = {'value1': '3', 'value2': '4'}
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'result': '12.0'})

        record = Record.objects.get(user=user, operation=self.operation)
        self.assertEqual(record.user_balance, 90)  # user balance should be reduced by operation cost
        self.assertEqual(record.operation_response, '12.0')

class DivisionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operation = Operation.objects.create(type='division', cost=3)
        self.url = reverse('division')

    def test_division(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass')
        user.credit = 100
        user.save()

        data = {'value1': '12', 'value2': '4'}
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'result': '3.0'})

        record = Record.objects.get(user=user, operation=self.operation)
        self.assertEqual(record.user_balance, 90)
        self.assertEqual(record.operation_response, '3.0')

class SubtractionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operation = Operation.objects.create(type='subtraction', cost=2)
        self.url = reverse('subtraction')

    def test_subtraction(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass')
        user.credit = 100
        user.save()

        data = {'value1': '10', 'value2': '5'}
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'result': '5.0'})

        record = Record.objects.get(user=user, operation=self.operation)
        self.assertEqual(record.user_balance, 90)
        self.assertEqual(record.operation_response, '5.0')

class SquareRootTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operation = Operation.objects.create(type='square_root', cost=2)
        self.url = reverse('square_root')

    def test_square_root(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass')
        user.credit = 100  # set initial credit to 100
        user.save()

        data = {'value1': '16'}
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'result': '4.0'})

        record = Record.objects.get(user=user, operation=self.operation)
        self.assertEqual(record.user_balance, 80)  # user balance should be reduced by operation cost
        self.assertEqual(record.operation_response, '4.0')

class RandomStringTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.operation = Operation.objects.create(type='random_string', cost=25)
        self.url = reverse('random_string')

    def test_random_string(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'length': 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()['result']
        self.assertEqual(len(result), 10)

        record = Record.objects.get(user=self.user, operation=self.operation)
        self.assertEqual(record.amount, 25)
        self.assertEqual(record.user_balance, 75)
        self.assertEqual(record.operation_response, result)



