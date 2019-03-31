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




class Clock(AsyncJsonWebsocketConsumer):

    COUNT=1
    
    async def connect(self): 
        await self.accept()
     
    async def receive_json(self, content):
        print("RECEIVED: ", content)
        await self.send_json({"txt": "hello world"})
        #await self.close(code=4123)
    
        for i in range(0,10):
            await asyncio.sleep(1)
            await self.send_json({"clock": self.COUNT })
            self.COUNT+=1
    
    async def disconnect(self, close_code):
        print("Websocket closed", close_code)
    



