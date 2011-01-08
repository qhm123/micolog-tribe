# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from common import models

def index(request): 
    
    template = loader.get_template('welcome/templates/index.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))

def about(request):
    manual = models.Tribe.getManual()
    
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