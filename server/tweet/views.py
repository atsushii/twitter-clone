from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Tweet
from tweet.serializers import TweetSerializer


class BaseTweetView(generics.RetrieveAPIView,
                    generics.UpdateAPIView,
                    generics.DestroyAPIView,
                    generics.ListAPIView
                    ):

    lookup_url_kwarg = 'tweet_id'
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        user = self.request.user
        return Tweet.objects.filter(user=user)


class CreateTweetView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetsListView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        user = self.request.user
        return Tweet.objects.filter(user=user)


class TweetDetailView(BaseTweetView):
    def get_object(self):
        queryset = self.get_queryset()
        query_filter = {self.lookup_field: self.kwargs['tweet_id']}
        obj = get_object_or_404(queryset, **query_filter)
        self.check_object_permissions(self.request, obj)
        return obj


class TweetUpdateView(BaseTweetView):
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.tweet = request.data.get('tweet')
        instance.save()
        data = {
            'tweet': request.data.get('tweet')
        }
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class TweetDeleteView(BaseTweetView):
    pass
