# -*- coding: utf-8 -*

from xmlrpclib import datetime

from appengine_django.models import BaseModel
from google.appengine.ext import db

from taggable import Taggable
from rssa.feedfetch import FeedParser
from common.timezone import UTC0, to_utc8

class Tribe(BaseModel):
    """部落全局设置模型"""
    
    manual = db.TextProperty(default='')    # 手册说明文本，介绍部落
    
    @classmethod
    def getManual(cls):
        if Tribe.all().get() is None:
            tribe = Tribe()
            tribe.put()
        return Tribe.all().get().manual

class Blog(Taggable, BaseModel):
    """博客模型"""
       
    user = db.UserProperty(required=True)
    name = db.StringProperty(required=True)
    category = db.StringProperty(required=True)         # NOTE: 废弃不用了
    link = db.StringProperty(required=True)
    pic = db.BlobProperty(required=True)
    add_date = db.DateTimeProperty(auto_now_add=True)
    rate = db.FloatProperty(default=0.0)
    rate_count = db.IntegerProperty(default=0)
    rate_ips = db.StringListProperty(default=None)
    feedurl = db.StringProperty()
    
    def __init__(self, parent=None, key_name=None, app=None, **entity_values):
        """初始化，主要用于初始化Taggable。"""
        
        BaseModel.__init__(self, parent, key_name, app, **entity_values)
        Taggable.__init__(self)
    
    @classmethod
    def add(cls, user, name, category, link, pic, tags='', feedurl=''):
        """添加一个博客。"""
        
        blog = Blog(user=user, name=name, category=category, link=link, pic=pic)
        blog.feedurl = feedurl
        blog.put()
        
        blog.tags = tags;
        blog.put()
        
        # TODO: 检测feedurl是否可以解析，不可以解析弹出错误报告。
        try:
            feedparser = FeedParser(feedurl)
            Feed.add(user, feedurl, feedparser.title, feedparser.subtitle, feedparser.link, blog)
        except:
            pass
                    
    @classmethod
    def admin_add(cls, mail, name, category, link, pic, tags='', feedurl=''):
        """管理员添加方法。"""
        
        Blog.add(db.users.User(mail) ,name, category, link, pic, tags, feedurl)
        
    def update(self, name, category, link, tags, feedurl):
        """更新博客基本信息。"""
        
        self.name = name
        self.category = category
        self.link = link
        self.tags = tags
        self.put()
        
        # 如果feedurl地址变更则更新Feed实体，否则不做操作。
        if feedurl != self.feedurl:
            feed = Feed.all().filter('blog =', self).get()
            # TODO: 检测feedurl是否可以解析，不可以解析弹出错误报告。
            if feed:
                try:
                    feedparser = FeedParser(feedurl)
                    feed.update(feedurl, feedparser.title, feedparser.subtitle, feedparser.link)
                    self.feedurl = feedurl
                    self.put()
                except:
                    pass
            else:
                try:
                    feedparser = FeedParser(feedurl)
                    Feed.add(self.user, feedurl, feedparser.title, feedparser.subtitle, feedparser.link, self)
                    self.feedurl = feedurl
                    self.put()
                except:
                    pass
        
    def update_pic(self, pic):
        """更新博客图片信息。"""
        
        self.pic = db.Blob(pic)
        self.put()
        
    def add_rate(self, score, ip):
        """给博客投票一票。会进行IP检测，如果IP存在与该博客的IP列表，则投票失败。"""
        
        if ip in self.rate_ips:
            return {"success": False, "rate": self.rate, "rate_count": self.rate_count}
        self.rate_ips.append(ip)
        self.rate = (self.rate * self.rate_count + score) / (self.rate_count + 1)
        self.rate_count += 1
        self.put()
        
        return {"success": True, "rate": self.rate, "rate_count": self.rate_count}
    
class Feed(BaseModel):
    """博客Feed/RSS模型。"""
    
    user = db.UserProperty(required=True)
    feed_url = db.StringProperty(required=True)
    title = db.StringProperty()
    subtitle = db.StringProperty()
    link = db.StringProperty()
    blog = db.ReferenceProperty(Blog)
    
    @classmethod
    def add(cls, user, url, title='', subtitle='', link='', blog=None):
        """添加Feed实体。"""
        
        feed = Feed(user=user, feed_url=url)
        feed.title = title
        feed.subtitle = subtitle
        feed.link = link
        feed.blog = blog
        feed.put()
        
    def update(self, url, title='', subtitle='', link=''):
        """更新Feed实体，不能更改user和blog属性。"""
        
        self.url = url
        self.title = title
        self.subtitle = subtitle
        self.link = link
        self.put()

class Entry(BaseModel):
    """Feed中的文章Entry模型。"""
    
    perid = db.StringProperty()
    title = db.StringProperty()
    link = db.StringProperty()
    date = db.DateTimeProperty()
    description = db.TextProperty()
    content = db.TextProperty()
    feed = db.ReferenceProperty(Feed)
    rate_count = db.IntegerProperty(default=0)
    rate_ips = db.StringListProperty(default=None)
    
    @classmethod
    def add(cls, perid, title, link, updated, description, content, feed):
        """添加Feed中的Entry实体。"""
        
        entry = Entry.all().filter('perid =', perid).get()
        if not entry:
            entry = Entry()
            entry.perid = perid
            entry.title = title
            entry.link = link
            
            #Tue, 09 Nov 2010 08:33:11 +0000
            #entry.date = datetime.datetime.strptime(updated, '%a, %d %b %Y %H:%M:%S +0000')
            # NOTE: Micolog默认feed是utc0， 所以这里对应转换成utc8， 考虑改进
            entry.date = to_utc8(datetime.datetime(updated[0], updated[1], updated[2], updated[3], updated[4], updated[5], tzinfo=UTC0()))
            entry.description = description
            entry.content = content
            entry.feed = feed
            entry.put()
            
    def add_rate(self, ip):
        """给Entry投一票。会进行IP检测，如果IP存在与该博客的IP列表，则投票失败。"""
        
        if ip in self.rate_ips:
            return {"success": False, "rate_count": self.rate_count}
        self.rate_count += 1
        self.rate_ips.append(ip)
        self.put()
        return {"success": True, "rate_count": self.rate_count}
        
class Category(BaseModel):
    """博客分类模式，已经废弃不用。"""
    
    cateid = db.IntegerProperty()
    name = db.StringProperty()
    blog = db.ReferenceProperty(Blog)