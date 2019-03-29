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
        # Called on connection.
        # To accept the connection call:
        await self.accept()
        
        while(True):
            await asyncio.sleep(1)
            await self.send_json({"clock": self.COUNT })
            self.COUNT+=1
            
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        #await self.accept("subprotocol")
        # To reject the connection, call:
        #await self.close()
    
    async def receive_json(self, content):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        print("RECEIVED: ", content)
        await self.send_json({"txt": "hello world"})
        # Or, to send a binary frame:
        #await self.close()
        # Or add a custom WebSocket error code!
        #await self.close(code=4123)
    
    
    async def disconnect(self, close_code):
        # Called when the socket closes
        print("Websocket closed", close_code)
            
    



