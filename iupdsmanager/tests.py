# from django.test import TestCase
# from rest_framework.test import APIRequestFactory

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/v1/create_user/'
        data = {'email': 'sunday@gmail.com', 'password': '1234567', 'password_confirmation': '1234567'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'email': 'sunday@gmail.com1', 'password': '1234567',
                                         'password_confirmation': '1234567'})
