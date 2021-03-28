from rest_framework import serializers, viewsets, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.serializers import ChatMessageSerializer, ThreadSerializer
from core.models import Thread, ChatMessage


class ThreadListView(generics.ListAPIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class TreadDetailView(generics.RetrieveAPIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        target_username = self.kwargs.get('username')
        obj = Thread.objects.get_or_new(self.request.user, target_username)
        return obj


class SendMessageView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        target_username = self.kwargs.get('username')
        obj = Thread.objects.get_or_new(self.request.user, target_username)
        return obj

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            response = {
                'message': f"thread doesn't exist with {self.kwargs.get('username')}"
            }
            return Response(response)

        message = request.data.get('message')
        data = {
            'thread': instance,
            'sender': self.request.user,
            'message': message
        }

        obj = ChatMessage.objects.create(**data)

        return Response({'id': obj.id, 'message': obj.message})
