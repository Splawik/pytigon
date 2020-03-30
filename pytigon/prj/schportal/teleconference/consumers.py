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
        
        status = 0
        if slug not in GLOBAL_NODES:
            GLOBAL_NODES[slug] = Node(slug, [self])
        else:
            if GLOBAL_NODES[slug].clients[0]==None:
               GLOBAL_NODES[slug].clients[0] = self
            else:
                GLOBAL_NODES[slug].clients.append(self)
                if len(GLOBAL_NODES[slug].clients) > 2:
                    status = 2
                else:
                    status = 1
    
        self.current_node = GLOBAL_NODES[slug]
    
        #await self.send(text_data=["owner", "guest", "magic_overload"][status])
        await self.send(text_data=["owner", "guest", "guest"][status])
    
        #if len(self.current_node.clients) == 1:
        #    await self.send(text_data="owner")
        #elif len(self.current_node.clients) > 2:
        #    await self.send(text_data="magic_overload")
        #else:
        #    await self.send(text_data="guest")
     
    
    async def disconnect(self, close_code):
        if self.current_node.clients[0] == self:
           self.current_node.clients[0] = None
        else:
            self.current_node.clients.remove(self)
        print("DDDDDDDDDDDDDDDDDIIIIIIIIIIIISSSSSSSSSSCONNECT")
    
    async def receive(self, text_data, bytes_data=None):
        if self == self.current_node.clients[0]:
            for client in self.current_node.clients[1:]:
                if client == None:
                    continue
                await client.send(text_data=text_data)    
        else:
            if self.current_node.clients[0]:
                await self.current_node.clients[0].send(text_data=text_data)
            
        #for client in self.current_node.clients:
        #    if client is self:
        #        continue
        #    if client == None:
        #        continue
        #    await client.send(text_data=text_data)    
    
    
    


 
