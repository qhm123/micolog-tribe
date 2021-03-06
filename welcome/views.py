# -*- coding: utf-8 -*

import urllib2
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse

from google.appengine.api import users, memcache, taskqueue

from common.BeautifulSoup import BeautifulSoup
from common import models
from talk.models import TalkLog
from common.helper import requires_admin

def index(request):
    
    blog = models.Blog.all().order('-add_date').get()
    entries = models.Entry.all().order('-date').fetch(limit=5)
    talks = TalkLog.all().order('-time').fetch(limit=5)
    msgs = (':'.join(talk.msg.split(':')[1:]) for talk in talks)
    
    template = loader.get_template('welcome/templates/index.html')
    context = RequestContext(request, {
        'blog': blog,
        'entries': entries,
        'msgs': msgs,
    })
    
    return HttpResponse(template.render(context))

def about(request):
    manual = models.Tribe.getManual()
    
    template = loader.get_template('welcome/templates/about.html')
    context = RequestContext(request, {
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
        context = RequestContext(request, {
            "blog": blog,
            'showmail': False,
        })
        
        return HttpResponse(template.render(context))
    else:
        user = users.get_current_user()
        if user:
            link = request.POST.get('link', '')
            if not link.startswith('http://'):
                link = 'http://' + link
            feedurl = link + '/feed'
            
            try:
                img = urllib2.urlopen("http://www.shrinktheweb.com/xino.php?stwembed=1&stwaccesskeyid=96a7847ecf72707&stwsize=lg&stwurl=%s" %link).read()
            except Exception, e:
                logging.error('fetch shrinktheweb failed, url is %s' % link)
                logging.error(e)
                img = ''
                
            try:
                data = urllib2.urlopen(link).read()
                soup = BeautifulSoup(data)
                name = soup.html.head.title.text
                
                meta = soup.html.head.find('meta', {'name': 'Keywords'})
                if meta:
                    tags = meta['content']
                else:
                    tags = u''
            except:
                name = 'unkonw'
                tags = u''
                logging.error('parse html error %s.' % (link,))
            
            blog = models.Blog.all().filter('user =', user).get()
            if not blog:
                models.Blog.add(user, name, img, link, tags, feedurl)
            elif blog:
                blog.update(name, link, tags, feedurl)
                blog.update_pic(img)
            
        return HttpResponseRedirect(reverse('welcome.views.index'))

@requires_admin
def refresh_thumbnail(request):
    blogs = models.Blog.all().fetch(limit=1000)
    for blog in blogs:
        link = blog.link
        try:
            img = urllib2.urlopen("http://www.shrinktheweb.com/xino.php?stwembed=1&stwaccesskeyid=96a7847ecf72707&stwsize=lg&stwurl=%s" %link).read()
            blog.update_pic(img)
        except:
            logging.error("admin refresh all thumbnail failed in link %s" %link)
            
    return HttpResponse()

@requires_admin
def admin_add(request):
    """管理员专用：管理员添加博客。"""
    
    if request.method == 'GET':
        template = loader.get_template('welcome/templates/add.html')
        context = RequestContext(request, {
            'showmail': True,
        })
        
        return HttpResponse(template.render(context))
    else:
        mail = request.POST.get('mail', '')
        link = request.POST.get('link', '')
        if not link.startswith('http://'):
            link = 'http://' + link
        feedurl = link + '/feed'
        
        try:
            img = urllib2.urlopen("http://www.shrinktheweb.com/xino.php?stwembed=1&stwaccesskeyid=96a7847ecf72707&stwsize=lg&stwurl=%s" %link).read()
        except Exception, e:
            logging.error('fetch shrinktheweb failed, url is %s' % link)
            logging.error(e)
            img = ''
        
        try:
            data = urllib2.urlopen(link).read()
            soup = BeautifulSoup(data)
            name = soup.html.head.title.text
            
            meta = soup.html.head.find('meta', {'name': 'Keywords'})
            if meta:
                tags = meta['content']
            else:
                tags = u''
        except:
            name = 'unkonw'
            tags = u''
            logging.error('parse html error')
        
        models.Blog.admin_add(mail, name, img, link, tags, feedurl)
        
        return HttpResponseRedirect(reverse('welcome.views.admin_add'))
    
def refresh_tags(request):
    
    blogkeys = [blog.key() for blog in models.Blog.all().fetch(limit=1000)]
    if blogkeys and len(blogkeys) > 0:
        memcache.set('blogkeys', blogkeys)
        queue = taskqueue.Queue('background-processing')
        queue.add(taskqueue.Task(url='/refresh_tags_worker'))
    
    return HttpResponse()

def refresh_tags_worker(request):
    
    blogkeys = memcache.get('blogkeys')
    if blogkeys is None:
        return HttpResponse()
    if len(blogkeys) > 0:
        blogkey = blogkeys.pop()
    if len(blogkeys) > 0:
        memcache.set('blogkeys', blogkeys)
        queue = taskqueue.Queue('background-processing')
        queue.add(taskqueue.Task(url='/refresh_tags_worker'))
        
    blog = models.Blog.get(blogkey)
    link = blog.link
    feedurl = blog.feedurl
    try:
        data = urllib2.urlopen(link).read()
        soup = BeautifulSoup(data)
    except:
        logging.error('parse html error %s.' % (link,))
    try:
        name = soup.html.head.title.text
    except:
        name = blog.name
        logging.error('parse name error %s.' % (link,))
    try:
        meta = soup.html.head.find('meta', {'name': 'Keywords'})
        if meta:
            tags = meta['content']
        else:
            tags = u''
    except:
        tags = u''
        logging.error('parse keywords error %s.' % (link,))
    
    blog.update(name, link, tags, feedurl)
    
    return HttpResponse()
