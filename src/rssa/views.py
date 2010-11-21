# -*- coding: utf-8 -*

import logging
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from google.appengine.api import users

import models
from blogshow.models import Blog
from feedfetch import FeedParser
from common.helper import requires_admin

def index(request):
    
    # 只显示最新的20个RSS内容
    entries = models.Entry.all().order('-date').fetch(limit=20)
    weekago = datetime.today() + timedelta(days=-7)
    hotentries = models.Entry.all().filter('date >', weekago).fetch(limit=3)
    
    template = loader.get_template('rssa/templates/index.html')
    context = Context({
        "entries": entries,
        "hotentries": hotentries,
    })
    
    return HttpResponse(template.render(context))

@requires_admin
def refresh_db_feedentry(request):
    for entry in models.Entry.all().fetch(limit=1000):
        entry.rate_count = 0;
        entry.rate_ips = []
        entry.put()
        
    return HttpResponse()

def add(request):
    user = users.get_current_user()
    if not user:
        login_url = users.create_login_url(reverse('rssa.views.add'))
        return HttpResponseRedirect(login_url)
        
    if request.method == 'GET':
        feed = models.Feed.all().filter('user =', user).get()
        
        template = loader.get_template('rssa/templates/add.html')
        context = Context({
            "feed": feed,
        })
        
        return HttpResponse(template.render(context))
    else:
        url = request.POST.get('feed_url')
        if url:
            feed = FeedParser(url)
            models.Feed.add(user, url, feed.title, feed.subtitle, feed.link)
        return HttpResponseRedirect(reverse('rssa.views.add'))
    
def rate(request):
    entryid = request.POST.get('entryid')
    if entryid is None:
        return HttpResponse(status=400)
    entry = models.Entry.get_by_id(int(entryid))
    if entry is None:
        return HttpResponse(status=400)
    ip = request.META['REMOTE_ADDR']
    success = entry.add_rate(ip)
    if success:
        return HttpResponse(success)
    else:
        return HttpResponse(success)

#@requires_admin
def fetch_feed(request):
    feeds = models.Feed.all().fetch(limit=1000)

    for feed in feeds:
        try:
            fp = FeedParser(feed.feed_url)
            for e in fp.entries:
                models.Entry.add(e.id, e.title, e.link, e.updated, e.description, e.content, feed)
        except:
            logging.error("fetch feed failed, url: %s.", feed.feed_url)

    return HttpResponse()

@requires_admin
def add_all(request):
    added_link = [feed.link for feed in models.Feed.all().fetch(limit=1000)]
    
    for blog in Blog.all().fetch(limit=1000):
        if blog.link not in added_link:
            feed_url = blog.link + '/feed'
            
            fp = None
            try:
                fp = FeedParser(feed_url)
            except:
                pass
            if fp:
                models.Feed.add(blog.user, feed_url, fp.title, fp.subtitle, fp.link)
            
    return HttpResponse()