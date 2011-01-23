# coding: utf-8

from google.appengine.api import xmpp, memcache, channel
from google.appengine.ext import db

from django.utils import simplejson

import models as talk_models

def send(msg, sender=None):
    """群发消息。现在都返回成功。
    
    args: sender是Email地址。使用sender去除发送者。
    """
    
    if sender:
        user = db.users.User(email=sender)
    else:
        user = db.users.User(email='web@web.com')
    talk_models.TalkLog.add(user, msg)
    
    users = talk_models.TalkStatus.all().fetch(limit=1000)
    jids = [user.user.email() for user in users if user.user.email() != sender]
    xmpp.send_message(jids=jids, body=msg)

def channel_send(msg):
    channel_ids = memcache.get('channel_ids')
    if channel_ids:
        json = simplejson.dumps({'msg': msg,})
        for channel_id in channel_ids:
            channel.send_message(channel_id, json)
        
def recieve():
    pass

def invite(jid):
    xmpp.send_invite(jid)
    
if __name__ == '__main__':
    send()