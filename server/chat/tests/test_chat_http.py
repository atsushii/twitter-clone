from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model


PASSWORD = '1234Test'

THREAD_LIST_URL = reverse('chat:thread-list')


def chat_detail_url(username):
    return reverse('chat:detail', args=[username])


def send_message_url(username):
    return reverse('chat:send-message', args=[username])


def create_user(username='sample'):
    return get_user_model().objects.create_user(
        username=username,
        password=PASSWORD
    )


class AuthenticatedUserChatTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_user_can_list_thread(self):
        target_user = create_user('target_user')
        detail_url = chat_detail_url(target_user.username)
        self.client.get(detail_url)
        response = self.client.get(THREAD_LIST_URL)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)

    def test_user_can_retrieve_detail(self):
        target_user = create_user('target_user')
        detail_url = chat_detail_url(target_user.username)
        message_url = send_message_url(target_user.username)
        payload = {
            'message': 'hello'
        }
        self.client.post(message_url, payload)
        response = self.client.get(detail_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['first'], self.user.username)
        self.assertEqual(response.data['second'], target_user.username)

    def test_user_send_message(self):
        target_user = create_user('target_user')
        chat_detail_url(target_user.username)
        message_url = send_message_url(target_user.username)
        payload = {
            'message': 'hello'
        }
        response = self.client.post(message_url, payload)
        target_client = APIClient()
        target_client.force_authenticate(target_user)
        detail_url = chat_detail_url(self.user.username)
        target_user_response = target_client.get(detail_url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(payload['message'], response.data['message'])
        self.assertIn(payload['message'], target_user_response.data['threads'][0])


class PublicUserChatTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

    def test_user_cannot_create_thread(self):
        target_user = create_user('target_user')
        detail_url = chat_detail_url(target_user.username)
        response = self.client.get(detail_url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_send_message(self):
        target_user = create_user('target_user')
        chat_detail_url(target_user.username)
        message_url = send_message_url(target_user.username)
        payload = {
            'message': 'hello'
        }
        response = self.client.post(message_url, payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_retrieve_detail(self):
        target_user = create_user('target_user')
        detail_url = chat_detail_url(target_user.username)
        response = self.client.get(detail_url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_list_thread(self):
        response = self.client.get(THREAD_LIST_URL)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
