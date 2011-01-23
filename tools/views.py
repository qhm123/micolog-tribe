# coding: utf-8

import re

from django import http
from django.template import Context, loader

from common.models import Blog

IP = '203.208.39.104'

def hosts(request):
    
    links = (blog.link[7:].encode('utf8').split('/')[0] for blog in Blog.all().fetch(limit=1000) if 'appspot.com' in blog.link)
    
    template = loader.get_template('tools/templates/hosts.html')
    context = Context({
        'links': links,
        'ip': IP,
    })
    
    return http.HttpResponse(template.render(context))