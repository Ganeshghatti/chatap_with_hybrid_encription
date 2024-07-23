import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .crypto_utils import encrypt_message, decrypt_message, private_key, public_key

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Encrypt the message
        iv, encrypted_message, enc_session_key = encrypt_message(message, public_key)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': encrypted_message,
                'iv': iv,
                'enc_session_key': enc_session_key
            }
        )

    async def chat_message(self, event):
        encrypted_message = event['message']
        iv = event['iv']
        enc_session_key = event['enc_session_key']

        # Decrypt the message
        message = decrypt_message(iv, encrypted_message, enc_session_key, private_key)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
