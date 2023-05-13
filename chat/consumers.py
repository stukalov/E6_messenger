import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls import reverse


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_url = None
        self.group_name = None
        self.room_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["chat_room_id"]
        self.group_name = f"chat_room_id-{self.room_name}"

        if self.user.is_authenticated:
            self.user_url = reverse('messenger.user.view', kwargs={'pk': self.user.pk})
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "data": {
                    "message": message,
                    "user": {
                        "id": self.user.id,
                        "name": self.user.username,
                        "url": self.user_url,
                    },
                }
            }
        )

    async def chat_message(self, event):
        if self.scope["user"].pk != event["data"]["user"]["id"]:
            await self.send(text_data=json.dumps(event["data"]))

        