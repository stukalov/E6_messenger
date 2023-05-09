from django.urls import re_path, path

from chat import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:chat_room_id>", consumers.ChatConsumer.as_asgi()),
]
