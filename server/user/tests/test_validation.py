from rest_framework.test import APITestCase
from rest_framework import serializers

from django.urls import reverse
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer, LoginSerializer

PASSWORD = '1234Test'

REGISTER_USER_URL = reverse('user:register')
LOGIN_USER_URL = reverse('user:log-in')


def create_user(**kwargs):
    return get_user_model().objects.create_user(
        username='sample',
        password=PASSWORD
    )


class ValidationTests(APITestCase):
    def test_validation_with_valid_password(self):
        data = {
            'username': 'test',
            'password1': 'PAssword1',
            'password2': 'PAssword1'
        }
        response = UserSerializer(data=data)

        self.assertTrue(response.is_valid(), True)

    def test_validation_with_invalid_password_length(self):
        data = {
            'username': 'test',
            'password1': 'PAsswo1',
            'password2': 'PAsswo1'
        }
        with self.assertRaisesMessage(
                serializers.ValidationError,
                'password must be greater than 8'):
            response = UserSerializer(data=data)
            response.is_valid(raise_exception=True)

    def test_validation_with_invalid_password_isdigit(self):
        data = {
            'username': 'test',
            'password1': 'PAssworfs',
            'password2': 'PAssworfs'
        }
        with self.assertRaisesMessage(
                serializers.ValidationError,
                'password must be at least one numeral'):
            response = UserSerializer(data=data)
            response.is_valid(raise_exception=True)

    def test_validation_with_invalid_password_isupper(self):
        data = {
            'username': 'test',
            'password1': 'password1',
            'password2': 'password1'
        }
        with self.assertRaisesMessage(
                serializers.ValidationError,
                'password must be at least one uppercase'):
            response = UserSerializer(data=data)
            response.is_valid(raise_exception=True)

    def test_validation_with_invalid_password_islower(self):
        data = {
            'username': 'test',
            'password1': 'PASSWORD1',
            'password2': 'PASSWORD1'
        }
        with self.assertRaisesMessage(
                serializers.ValidationError,
                'password must be at least one lowercase'):
            response = UserSerializer(data=data)
            response.is_valid(raise_exception=True)

    def test_password_not_match(self):
        data = {
            'username': 'test',
            'password1': 'passworD1',
            'password2': 'passworD2'
        }

        with self.assertRaisesMessage(
                serializers.ValidationError, 'password should be match'):
            response = UserSerializer(data=data)
            response.is_valid(raise_exception=True)

    def test_validation_unable_to_login(self):
        data = {
            'username': 'test',
            'password': 'PASSword',
        }
        response = LoginSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            response.is_valid(raise_exception=True)
