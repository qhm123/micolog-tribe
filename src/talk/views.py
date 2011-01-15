# coding: utf-8

from django import http
from django.template import Context, loader
from django.core.urlresolvers import reverse

import xmpp

def index(request):
    """主页"""
    template = loader.get_template('talk/templates/index.html')
    context = Context({
    })
    
    return http.HttpResponse(template.render(context))

def send(request):
    """发送信息"""
    xmpp.test()
    
    return http.HttpResponseRedirect(reverse('talk.views.index'))

def recieve(request):
    """接收消息"""
    xmpp.recieve(request)
    
    