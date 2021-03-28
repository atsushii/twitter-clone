from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Tweet

PASSWORD = '1234Test'

TWEET_URL = reverse('tweet:create')
TWEET_LIST_URL = reverse('tweet:list')


def tweet_detail_url(tweet_id):
    return reverse('tweet:detail', args=[tweet_id])


def tweet_update_url(tweet_id):
    return reverse('tweet:update', args=[tweet_id])


def tweet_delete_url(tweet_id):
    return reverse('tweet:delete', args=[tweet_id])


def create_user():
    return get_user_model().objects.create_user(
        username='sample',
        password=PASSWORD
    )


class AuthenticatedUserTweetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.payload = {
            'tweet': 'test'
        }

    def test_authenticated_user_can_tweet(self):
        response = self.client.post(TWEET_URL, self.payload)
        tweet = Tweet.objects.get(id=response.data['id'])

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.payload['tweet'], tweet.tweet)

    def test_authenticated_user_can_list(self):
        self.client.post(TWEET_URL, self.payload)
        self.client.post(TWEET_URL, self.payload)

        response = self.client.get(TWEET_LIST_URL)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 2)

    def test_authenticates_user_can_retrieve_detail(self):
        response = self.client.post(TWEET_URL, self.payload)
        url = tweet_detail_url(response.data['id'])
        tweet = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, tweet.status_code)
        self.assertEqual(tweet.data['tweet'], self.payload['tweet'])
        self.assertEqual(tweet.data['id'], response.data['id'])

    def test_authenticated_user_can_delete(self):
        response = self.client.post(TWEET_URL, self.payload)
        delete_url = tweet_delete_url(response.data['id'])
        deleted_response = self.client.delete(delete_url)

        detail_url = tweet_detail_url(response.data['id'])
        no_content = self.client.get(detail_url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, deleted_response.status_code)
        self.assertEqual(status.HTTP_404_NOT_FOUND, no_content.status_code)

    def test_authenticated_user_can_update(self):
        response = self.client.post(TWEET_URL, self.payload)
        update_url = tweet_update_url(response.data['id'])
        update_payload = {
            'tweet': 'updated'
        }
        update_response = self.client.put(update_url, update_payload)
        detail_url = tweet_detail_url(response.data['id'])
        updated_tweet = self.client.get(detail_url)

        self.assertEqual(status.HTTP_200_OK, update_response.status_code)
        self.assertEqual(update_payload['tweet'], updated_tweet.data['tweet'])


class PublicUserTweetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'tweet': 'test'
        }

    def test_user_cannot_tweet(self):
        response = self.client.post(TWEET_URL, self.payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_list(self):

        response = self.client.get(TWEET_LIST_URL)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_retrieve_detail(self):
        url = tweet_detail_url(1)
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_delete(self):
        delete_url = tweet_delete_url(1)
        response = self.client.delete(delete_url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cannot_update(self):
        update_url = tweet_update_url(1)
        update_payload = {
            'tweet': 'updated'
        }
        response = self.client.put(update_url, update_payload)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)










