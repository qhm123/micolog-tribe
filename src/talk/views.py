# coding: utf-8

import logging

from django import http
from django.template import Context, loader
from django.core.urlresolvers import reverse

from google.appengine.api import xmpp
from google.appengine.ext import db

from common.helper import requires_admin
import models as talk_models
from common.models import Blog
import grouptalk


def index(request):
    """主页"""
    
    messages = talk_models.TalkLog.all().order('time').fetch(limit=10)
    users = talk_models.TalkStatus.all()
    
    template = loader.get_template('talk/templates/index.html')
    context = Context({
        'messages': messages,
        'users': users,
    })
    
    return http.HttpResponse(template.render(context))

def send(request):
    """网页发送信息。 """
    
    if request.method == 'POST':
        msg = request.POST.get('content')
        user = db.users.get_current_user()
        if user:
            grouptalk.send(msg, user.email())
        else:
            grouptalk.send(msg)
                
        return http.HttpResponse()

def recieve(request):
    """机器人接收消息，信息转发。"""
    
    try:
        message = xmpp.Message(request.POST)
#        message.reply('sender: %s' % message.sender)
        sender_mail = message.sender.split('/')[0]
#        message.reply('sender: %s' % sender_mail)
        grouptalk.send(message.body, sender_mail)
    except:
        logging.error('error send msg!')
        
def history(request):
    """聊天历史"""
    
    # TODO: 性能优化
    messages = talk_models.TalkLog.all().order('time').fetch(limit=10)
    
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
    