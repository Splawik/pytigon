#!/usr/bin/python

# -*- coding: utf-8 -*-
import os
import sys
import datetime
import json
import asyncio

from channels.consumer import AsyncConsumer, SyncConsumer

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, \
    JsonWebsocketConsumer, AsyncJsonWebsocketConsumer

from channels.generic.http import AsyncHttpConsumer




class teleconference(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = "default"
    
    async def connect(self):
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send_json({"hello": self.room_group_name})
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("DDDDDDDDDDDDDDDDDIIIIIIIIIIIISSSSSSSSSSCONNECT")
    
    async def receive_json(self, content):
        print("receive", content)
        if not 'ping' in content:        
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": content}
            )
    
    async def chat_message(self, event):
        message = event["message"]
        await self.send_json(message)
    
    



