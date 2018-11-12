#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from getpass import getpass
from os import environ
from twisted.mail import imap4 
from twisted.internet import reactor, protocol, defer
import email
from twisted.internet import ssl

from email.mime.text import MIMEText
import io
import logging 

logger = logging.getLogger(__name__)

def GetMailboxConnection(server, user, password, mailbox="inbox", mailbox2="outbox"):

    f = protocol.ClientFactory()
    f.user     = user.encode('utf-8')
    f.password = password.encode('utf-8')
    f.mailbox  = mailbox 
    f.mailbox2 = mailbox2

    class ConnectInbox(imap4.IMAP4Client):
        @defer.inlineCallbacks
        def serverGreeting(self, caps):
            yield self.login(self.factory.user, self.factory.password)
            yield self.select(self.factory.mailbox)
            self.factory.deferred.callback(self)

    f.protocol = ConnectInbox
    reactor.connectSSL(server, 993, f, ssl.ClientContextFactory())

    f.deferred = defer.Deferred()
    return f.deferred

        
@defer.inlineCallbacks
def get_unseen_messages(conn, callback):
    return conn.search(imap4.Query(unseen=True), uid=True).addCallback(list_messages, conn, callback)


@defer.inlineCallbacks
def send_test_message(conn, msg):
    logger.info("send: " + msg['Subject'])
    x = io.BytesIO(msg.as_string().encode('utf-8'))
    return conn.append(conn.factory.mailbox2, x).addCallback(final, conn)


def list_messages(result, conn, callback):
    if len(result)>0:
        messages = ",".join([ str(pos) for pos in result ])
        return conn.fetchBody(messages, uid=True).addCallback(fetch_msg, conn, messages, callback)
    else:
        final(None, conn)


def fetch_msg(result, conn, messages, callback):
    if result:
        logger.info("new messages")
        keys = sorted(result)
        for k in keys:
            for k2 in result[k]:
                callback(result[k][k2])
    else:
        print("Hey, an empty mailbox!")
    return conn.addFlags(messages, 'SEEN', uid=True).addCallback(final, conn)


def final(result, conn):    
    return conn.logout()


class IMAPClient():
    def __init__(self, server, username, password, inbox="inbox", outbox="outbox"):
        self.server = server  
        self.username =  username
        self.password = password
        self.inbox  = inbox
        self.outbox  =  outbox
        
    def save_to_sent(self, msg):
        return  GetMailboxConnection(self.server, self.username, self.password,mailbox2=self.outbox).addCallback(send_test_message, msg)

    def check_mails(self, callback):
        return GetMailboxConnection(self.server, self.username, self.password, self.inbox).addCallback(get_unseen_messages, callback)
        

if __name__=="__main__":
    server = 'imap.gmail.com'
    username = "abc@gmail.com"
    password = "abc"
    client  = IMAPClient(server, username, password, "inbox", "[Gmail]/Wysłane")

    msg = MIMEText("Hello world!")
    msg['Subject'] = 'Subject'
    msg['From'] = "abc"
    msg['To'] = "def"
    client.save_to_sent(msg)

    def callback(x):
        with open("x.dat", "w") as f:
            f.write(x)

    client.check_mails(callback)

    reactor.run()
