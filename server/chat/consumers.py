import json
from django.contrib.auth.models import User

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.auth import UserLazyObject, get_user
from urllib.parse import parse_qs


from core.models import Thread, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        await self.accept({
            'type': 'websocket.accept'
        })

        me = self.scope['user']
        target_user = self.scope['url_route']['kwargs']['username']
        thread_obj, _ = await self.get_thread(me, target_user)
        self.thread_obj = thread_obj
        chat_room = f'thread_{thread_obj.id}'
        self.chat_room = chat_room
        print(self.channel_name)
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        text = event.get('text', None)
        print('text')
        if text is not None:
            loaded_dict_data = json.loads(text)
            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            print('user', user)
            username = 'anonymous'
            if user.is_authenticated:
                username = user
            response = {
                'message': msg,
                'username': username
            }
            await self.create_chat_message(user, msg)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        await super().disconnect(event)

    @database_sync_to_async
    def get_thread(self, user, target_username):
        return Thread.objects.get_or_new(user, target_username)

    @database_sync_to_async
    def create_chat_message(self, user, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, sender=user, message=msg)
