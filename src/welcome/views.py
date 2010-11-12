# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

import blogshow.models as models
import helper

def index(request): 
    peoples = [{'avatar_url': helper.get_avatar_url(blog.user.email()), 'blog_url': deal_link(blog.link)} for blog in models.Blog.all().fetch(limit=1000)]
    
    template = loader.get_template('welcome/templates/index.html')
    context = Context({
        "peoples": peoples,
    })
    
    return HttpResponse(template.render(context))

def deal_link(link):
    if not link.startswith('http://'):
        link = 'http://' + link
        
    return link