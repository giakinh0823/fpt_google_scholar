from time import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import threading
import json
import asyncio
from asgiref.sync import sync_to_async


class WordCloudConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect')
        await self.accept()
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(room_name, self.channel_name)
        print(f"Kết nối vào {self.channel_name}")

    async def receive(self, text_data): 
        pass
    
    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(room_name, self.channel_name)
        print(f"Thoát khỏi {self.channel_name}")

    async def send_data(self, event):   
        await self.send(text_data=json.dumps({
            'labeltitle': event['labeltitle'],
            'datatitle': event['datatitle'],
        }))

    async def send_error(self, event):
        await self.send(text_data=json.dumps({
            'error': event['error']
        }))
        
