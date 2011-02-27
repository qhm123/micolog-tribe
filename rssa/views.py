# -*- coding: utf-8 -*

import logging
from datetime import datetime, timedelta

from django.http import HttpResponse
from django import http
from django.template import RequestContext, loader
from django.utils import simplejson
from django.conf import settings

from google.appengine.api import memcache, taskqueue, mail
from google.appengine.ext import db

from common import models
from feedfetch import FeedParser
from common.helper import requires_admin

def index(request):
    """RSSA聚合首页。"""
    
    top3 = memcache.get('top3')
    if top3 is None:
        # 因为GAE必须在采用其他排序顺序之前对不等式过滤器中的属性进行排序，所以采用手动排序
        weekago = datetime.today() + timedelta(days=-7)
        hotentries = models.Entry.all().filter('date >', weekago).fetch(limit=1000)
        top3 = sorted(hotentries, key=lambda e:(e.rate_count, e.date), reverse=True)[0:3]
        memcache.add('top3', top3)
    
    entries = memcache.get('entries')
    if entries is None:
        # 只显示最新的20个左右（根据实际过滤个数决定，考虑到用户不会注意到下边到底有几个）
        # RSS内容（过滤掉最热的）
        entries = [e for e in models.Entry.all().order('-date').fetch(limit=20) if e not in top3]
        memcache.add('entries', entries)
    
    template = loader.get_template('rssa/templates/index.html')
    context = RequestContext(request, {
        "entries": entries,
        "hotentries": top3,
    })
    
    return HttpResponse(template.render(context))

def rate(request):
    """投票。"""
    
    entryid = request.POST.get('entryid')
    if entryid is None:
        return HttpResponse(status=400)
    entry = models.Entry.get_by_id(int(entryid))
    if entry is None:
        return HttpResponse(status=400)
    ip = request.META['REMOTE_ADDR']
    success = entry.add_rate(ip)
    if success['success']:
        memcache.delete('top3')
        memcache.delete('entries')
        
        voter = u'有人'
        voter_link = '#'
        user = db.users.get_current_user()
        if user:
            vote_blog = models.Blog.all().filter('user =', user).get()
            if vote_blog:
                voter = '%s|%s' % (user, vote_blog.name)
                voter_link = vote_blog.link
            else:
                voter = '%s|%s' % (user, 'blog')
                voter_link = "http://micolog-tribe.qhm123.com"
            
        blog = entry.feed.blog
        to = blog.user.email()
        subject = u'有人给您的文章投票了，快去看看。'
        body = u'''您在 Micolog部落 上注册的博客：%s。
%s 通过"文章聚合"给您的文章《%s》投票了，快去看看。
您也可以给别人的文章投票，试试看。
http://micolog-tribe.qhm123.com
''' % (blog.name, voter, entry.title)
        html = u'''您在<a href="http://micolog-tribe.qhm123.com" target="_blank">Micolog部落</a>上注册的博客：<a href="%s" target="_blank">%s</a>。<br/>
<a href="%s" target="_blank">%s</a>通过"文章聚合"给您的文章《%s》投票了，快去<a href="http://micolog-tribe.qhm123.com/rssa" target="_blank">看看</a>。<br/>
您也可以给别人的文章投票，<a href="http://micolog-tribe.qhm123.com/rssa" target="_blank">试试看</a>。<br/>
''' % (blog.link, blog.name, voter_link, voter, entry.title)
        mail.send_mail(settings.MAILSENDER, to, subject, body, html=html)
        
        json = simplejson.dumps({"success": True, "rate_count": success['rate_count']})
        return HttpResponse(json, mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps({"success": False, "rate_count": success['rate_count']}), mimetype='application/json')

def feed(request):
    """最新文章订阅。"""
    
    entries = models.Entry.all().order('-date').fetch(10)
        
    template = loader.get_template('rssa/templates/rss.xml')
    context = RequestContext(request, {
        "entries": entries,
    })
    
    return HttpResponse(template.render(context), mimetype='application/rss+xml; charset=utf8')

#@requires_admin
def fetch_feed(request):
    """管理员和cron用，更新抓取所有Feed的文章。使用TaskQueue机制。"""   
    
    feeds = models.Feed.all().fetch(limit=1000)
    if len(feeds) > 0:
        memcache.set('feeds', feeds)
        queue = taskqueue.Queue('feed-fetch-queue')
        queue.add(taskqueue.Task(url='/rssa/fetch_feed_worker'))

    return HttpResponse()

def fetch_feed_worker(request):
    """task队列worker，更新一个Feed的所有Entry。"""

    feeds = memcache.get('feeds')
    if len(feeds) > 0:
        feed = feeds.pop()
    if len(feeds) > 0:
        memcache.set('feeds', feeds)
        queue = taskqueue.Queue('feed-fetch-queue')
        queue.add(taskqueue.Task(url='/rssa/fetch_feed_worker'))
    else:
#        memcache.delete('feeds')
        memcache.delete('top3')
        memcache.delete('entries')
        
    try:
        fp = FeedParser(feed.feed_url)
        for e in fp.entries:
            models.Entry.add(e.id, e.title, e.link, e.updated, e.description, e.content, feed)
    except Exception, e:
        logging.error("fetch feed failed, url: %s.", feed.feed_url)
        return http.HttpResponse()  # mock，返回抓取成功，不再retry。可以考虑设置task属性。
    
    return http.HttpResponse()

@requires_admin
def add_all(request):
    """管理员专用，根据博客信息，自动寻找Feed地址，并添加所有Feed信息到数据库。
    ---已废弃---。
    """
    
    added_blog = [feed.blog for feed in models.Feed.all().fetch(limit=1000)]
    
    for blog in models.Blog.all().fetch(limit=1000):
        if blog not in added_blog:
            if blog.link.endswith('/'):
                feed_url = blog.link + 'feed'
            else:
                feed_url = blog.link + '/feed'
            
            fp = None
            try:
                fp = FeedParser(feed_url)
            except:
                pass
            if fp:
                models.Feed.add(blog.user, feed_url, fp.title, fp.subtitle, fp.link, blog)
            
    return HttpResponse()

@requires_admin
def refresh_db_feedentry(request):
    """慎用！管理员专用，更新Entry所有实体的投票数和投票IP列表。"""
    for entry in models.Entry.all().fetch(limit=1000):
        entry.rate_count = 0;
        entry.rate_ips = []
        entry.put()
        
    return HttpResponse()

@requires_admin
def refresh_entry_rateips(request):
    
    for entry in models.Entry.all().order('-date').fetch(limit=20):
        entry.rate_ips = []
        entry.put()
        
    return HttpResponse()