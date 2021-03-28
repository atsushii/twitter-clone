from rest_framework import serializers

from core.models import Thread, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = ['id', 'message']
        read_only_fields = ['timestamp', 'id']


class ThreadSerializer(serializers.ModelSerializer):

    first = serializers.StringRelatedField()
    second = serializers.StringRelatedField()
    threads = serializers.StringRelatedField(many=True)

    class Meta:
        model = Thread
        fields = ['id', 'first', 'second', 'threads', 'updated']
        read_only_fields = ['id']
