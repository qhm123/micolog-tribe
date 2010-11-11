# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from google.appengine.api import users

import models
from feedfetch import FeedParser

def index(request):
    template = loader.get_template('rssa/templates/index.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))

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

def fetch_feed(request):
    feeds = models.Feed.all().fetch(limit=1000)

    # TODO: 添加已添加文章过滤
    for feed in feeds:
        fp = FeedParser(feed.feed_url)
        for e in fp.entries:
            models.Entry.add(e.title, e.link, e.updated, e.description, e.content, feed)

    return HttpResponse()