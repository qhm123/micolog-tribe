# coding: utf-8

import logging

from django import http
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.utils import simplejson

from google.appengine.api import xmpp, channel, memcache
from google.appengine.ext import db

from common.helper import requires_admin
import models as talk_models
from common.models import Blog
import grouptalk

def get_webemail(isnew=False):
    """获取webemail地址。"""
    
    # TODO: 如何销毁某一个webemail
    cur_webclient_id = memcache.get('cur_webclient_id')
    if cur_webclient_id is None:
        cur_webclient_id = 0
        memcache.add('cur_webclient_id', cur_webclient_id)
    else:
        if isnew:
            cur_webclient_id += 1
            memcache.set('cur_webclient_id', cur_webclient_id)
    email = 'web%d@web.com' % cur_webclient_id
    return email

def index(request):
    """主页"""
    
    messages = talk_models.TalkLog.all().order('-time').fetch(limit=10)
    messages = sorted(messages, key=lambda e:(e.time,), reverse=False)
    users = talk_models.TalkStatus.all()
    
    # 创建channel，并将channelID放入memcache。 
    user = db.users.get_current_user()
    if user:
        email = user.email()
    else:
        email = get_webemail(True)
    
    channel_ids = memcache.get('channel_ids')
    if channel_ids is None:
        channel_ids = [email]
        memcache.add('channel_ids', channel_ids)
    else:
        if email not in channel_ids:
            channel_ids.append(email)
            memcache.set('channel_ids', channel_ids)
        
    token = channel.create_channel(email)
    
    template = loader.get_template('talk/templates/index.html')
    context = Context({
        'messages': messages,
        'users': users,
        'token': token,
    })
    
    return http.HttpResponse(template.render(context))

def send(request):
    """网页发送信息。 """
    
    if request.method == 'POST':
        try:
            msg = request.POST.get('content')
            
            # 发送到机器人
            user = db.users.get_current_user()
            if user:
                grouptalk.send(msg, user.email())
            else:
                grouptalk.send(msg)
            
            # 发送到web客户端
            channel_ids = memcache.get('channel_ids')
            if channel_ids:
                json = simplejson.dumps({'msg': msg,})
                for channel_id in channel_ids:
                    channel.send_message(channel_id, json)
        except:
            logging.error('error web send msg!')
                
        return http.HttpResponse()

def recieve(request):
    """机器人接收消息，信息转发。"""
    
    try:
        message = xmpp.Message(request.POST)
        sender_mail = message.sender.split('/')[0]
        grouptalk.send(message.body, sender_mail)
#        message.reply(sender_mail)
        
        # 发送到web客户端
        channel_ids = memcache.get('channel_ids')
        if channel_ids:
            json = simplejson.dumps({'msg': message.body,})
            for channel_id in channel_ids:
                channel.send_message(channel_id, json)
    except:
        logging.error('error send msg!')
        
    return http.HttpResponse()
        
def online(request):
    
    user = db.users.get_current_user()
    if user:
        sender = user.email()
    else:
        sender = get_webemail()
    grouptalk.send('%s is online.' % sender, sender=None)
    
    return http.HttpResponse()

def offline(request):
    
    user = db.users.get_current_user()
    if user:
        sender = user.email()
    else:
        sender = get_webemail()
    grouptalk.send('%s is offline.' % sender, sender=None)
    
    return http.HttpResponse()
        
def history(request):
    """聊天历史"""
    
    # TODO: 性能优化
    messages = talk_models.TalkLog.all().order('-time').fetch(limit=10)
    messages = sorted(messages, key=lambda e:(e.time,), reverse=False)
    
    template = loader.get_template('talk/templates/history.html')
    context = Context({
        'messages': messages,
    })
    
    return http.HttpResponse(template.render(context))

@requires_admin
def init_talkstatus(request):
    """管理员专用！慎用！初始化TalkStatus数据模型。"""
    
    db.delete(talk_models.TalkStatus.all().fetch(limit=1000))
    
    blogs = Blog.all().fetch(limit=1000)
    for blog in blogs:
        talk_models.TalkStatus.add(user=blog.user, blog=blog)

    return http.HttpResponse()

@requires_admin
def init_talkstatus_test(request):
    """管理员**测试**专用！慎用！初始化TalkStatus数据模型。"""
    
    db.delete(talk_models.TalkStatus.all().fetch(limit=1000))
    
    talk_models.TalkStatus.add(user=db.users.User(email='qhm123@gmail.com'), blog=None)
    talk_models.TalkStatus.add(user=db.users.User(email='qhmtest@gmail.com'), blog=None)
    
    return http.HttpResponse()
    