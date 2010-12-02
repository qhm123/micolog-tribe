# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from common.models import Tribe
import blogshow.models as models
import helper

def index(request): 
    
    # 去掉全家福头像
    #peoples = [{'avatar_url': helper.get_avatar_url(blog.user.email()), 'blog_url': deal_link(blog.link)} for blog in models.Blog.all().fetch(limit=1000)]
    
    template = loader.get_template('welcome/templates/index.html')
    context = Context({
        #"peoples": peoples,
        #"people_count": len(peoples),
    })
    
    return HttpResponse(template.render(context))

def about(request):
    manual = Tribe.getManual()
    
    template = loader.get_template('welcome/templates/about.html')
    context = Context({
        'manual': manual,
    })
    
    return HttpResponse(template.render(context))

def gtalk(request):  
    template = loader.get_template('welcome/templates/chat.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))

def deal_link(link):
    if not link.startswith('http://'):
        link = 'http://' + link
        
    return link