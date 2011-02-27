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
        json = simplejson.dumps({'msg': msg, })
        for channel_id in channel_ids:
            channel.send_message(channel_id, json)
        
def recieve():
    pass

def invite(jid):
    xmpp.send_invite(jid)
    
def is_command(str):
    if str.startswith('//'):
        return True
    return False
    
def exec_command(message, str):
    cmd = str[2:]
    if cmd == "help":
        msg = """help:
        //online - 显示所有在线成员。"""
    elif cmd == "online":
        msg = "\n".join(get_online_list())
    else:
        msg = "command is invalid. 你可以输入//help 获得帮助。"
    message.reply(msg)
    
def get_online_list():
    talkstautses = talk_models.TalkStatus.all().fetch(limit=1000)
    return ["%s|%s" % (talkstate.user, talkstate.blog.name) for talkstate in talkstautses if xmpp.get_presence(talkstate.user.email())]
    
def online_list():
    talkstautses = talk_models.TalkStatus.all().fetch(limit=1000)
    
    return [{"talkstauts": talkstauts,
             "online": xmpp.get_presence(talkstauts.user.email())} for talkstauts in talkstautses]
    
if __name__ == '__main__':
    send()
