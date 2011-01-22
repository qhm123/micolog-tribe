# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from google.appengine.api import users, images
from google.appengine.ext import db

from common import models
from common.helper import requires_admin

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

def add(request):
    """添加一个博客。"""
    
    if request.method == 'GET':
        user = users.get_current_user()
        if not user:
            login_url = users.create_login_url(reverse('welcome.views.add'))
            return HttpResponseRedirect(login_url)
        blog = models.Blog.all().filter('user =', user).get()
        
        template = loader.get_template('welcome/templates/add.html')
        context = Context({
            "blog": blog,
            'showmail': False,
        })
        
        return HttpResponse(template.render(context))
    else:
        user = users.get_current_user()
        if user:
            name = request.POST.get('name', '')
            link = request.POST.get('link', '')
            if not link.startswith('http://'):
                link = 'http://' + link
            tags = request.POST.get('tags')
            feedurl = link + '/feed'
            
            blog = models.Blog.all().filter('user =', user).get()
            if not blog:
                models.Blog.add(user, name, link, tags, feedurl)
            elif blog:
                blog.update(name, link, tags, feedurl)
            
        return HttpResponseRedirect(reverse('welcome.views.index'))

@requires_admin
def admin_add(request):
    """管理员专用：管理员添加博客。"""
    
    if request.method == 'GET':
        template = loader.get_template('welcome/templates/add.html')
        context = Context({
            'showmail': True,
        })
        
        return HttpResponse(template.render(context))
    else:
        name = request.POST.get('name', '')
        mail = request.POST.get('mail', '')
        link = request.POST.get('link', '')
        if not link.startswith('http://'):
            link = 'http://' + link
        tags = request.POST.get('tags')
        feedurl = link + '/feed'
        
        models.Blog.admin_add(mail, name, link, tags, feedurl)
        
        return HttpResponseRedirect(reverse('welcome.views.admin_add'))
    
    
    