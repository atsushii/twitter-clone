from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

PASSWORD = 'test1234'

REGISTER_USER_URL = reverse('user:register')
LOGIN_USER_URL = reverse('user:log-in')


def create_user(**kwargs):
    return get_user_model().objects.create_user(
        username='sample',
        password=PASSWORD
    )


class AuthenticationTest(APITestCase):
    def test_user_can_register(self):
        response = self.client.post(
            REGISTER_USER_URL, data={
                'username': 'sample',
                'password1': PASSWORD,
                'password2': PASSWORD
            }
        )
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], user.username)
        self.assertTrue(user.check_password(PASSWORD))

    def test_register_user_exist(self):
        payload = {
            'username': 'sample',
            'password1': PASSWORD,
            'password2': PASSWORD
        }
        create_user(**payload)
        response = self.client.post(REGISTER_USER_URL, data=payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_can_login(self):
        user = create_user()
        response = self.client.post(
            LOGIN_USER_URL, data={
                'username': user.username,
                'password': PASSWORD
            }
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(user.username, response.data['username'])
        self.assertEqual(user.id, response.data['id'])

    def test_login_user_not_exist(self):
        response = self.client.post(
            LOGIN_USER_URL, data={
                'username': 'sample',
                'password': PASSWORD
            }
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
