from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from chat.serializers import ChatMessageSerializer, ThreadSerializer
from core.models import Thread


class ChatMessage(generics.GenericAPIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        target_username = self.kwargs.get('username')
        obj, created = Thread.objects.get_or_new(self.request.user, target_username)
        if obj is None:
            return Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




