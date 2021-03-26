from rest_framework import serializers

from core.models import Tweet


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('id', 'tweet', 'created_date')
        read_only_fields = ('id', 'created_date')
