from rest_framework import serializers

from core.models import Thread, ChatMessage
from user.serializers import UserSerializer


class ThreadSerializer(serializers.ModelSerializer):

    first = UserSerializer()
    second = UserSerializer()

    class Meta:
        model = Thread
        fields = '__all__'
        depth = 1


class ChatMessageSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer()

    class Meta:
        model = ChatMessage
        fields = '__all__'
        depth = 1