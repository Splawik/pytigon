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

GLOBAL_NODES = {}

class Node(object):
    def __init__(self, name, clients=[]):
        self.name = name
        self.clients = clients

    def __repr__(self):
        return "Node '{0}'".format(self.name)

 


class teleconference(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_node = None
    
    async def connect(self):
        global GLOBAL_NODES
        slug = "default"
    
        await self.accept()
    
        if slug not in GLOBAL_NODES:
            GLOBAL_NODES[slug] = Node(slug, [self])
        else:
            GLOBAL_NODES[slug].clients.append(self)
    
        self.current_node = GLOBAL_NODES[slug]
    
        if len(self.current_node.clients) == 1:
            await self.send(text_data="owner")
        elif len(self.current_node.clients) > 2:
            await self.send(text_data="magic_overload")
        else:
            await self.send(text_data="guest")
     
    
    async def disconnect(self, close_code):
        self.current_node.clients.remove(self)
    
    async def receive(self, text_data, bytes_data=None):
        for client in self.current_node.clients:
            if client is self:
                continue
            await client.send(text_data=text_data)    
    
        print("receive: ", text_data)
    
        #text_data_json = json.loads(text_data)
        #message = text_data_json["message"]
        #print(message)
        #await self.save_chat(message)
        # print(text_data_json,self.scope["user"])
    
        # Send message to room group
        #await self.channel_layer.group_send(
        #    self.room_group_name,
        #    {
        #        "type": "chat_message",
        #        "message": message,
        ##        "username": self.scope["user"].username,
        #    },
        #)
    
        # Receive message from room group
    
    #async def chat_message(self, event):
    #    message = event["message"]
    #    print(message)
    #    # Send message to WebSocket
    #    await self.send(
    #        text_data=json.dumps({"message": message, "user": event["username"]})
    #    )
    
    #@database_sync_to_async
    #async def save_chat(self, message):
    #    #if "AnonymousUser" != str(self.scope["user"]):
    #    #    room = Room.objects.last()
    #    #    msg = ChatMessage.objects.create(
    #    #        room=room, user=self.scope["user"], message=message
    #    #    )
    #    return True
    
    


 
