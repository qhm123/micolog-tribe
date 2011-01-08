# -*- coding: utf-8 -*

from xmlrpclib import datetime

from appengine_django.models import BaseModel
from google.appengine.ext import db

from common.timezone import UTC0, to_utc8

class Tribe(BaseModel):
    manual = db.TextProperty(default='')
    
    @classmethod
    def getManual(cls):
        if Tribe.all().get() is None:
            tribe = Tribe()
            tribe.put()
        return Tribe.all().get().manual

class Blog(BaseModel):
    user = db.UserProperty(required=True)
    name = db.StringProperty(required=True)
    category = db.StringProperty(required=True)
    link = db.StringProperty(required=True)
    pic = db.BlobProperty(required=True)
    tags = db.StringProperty(default='')
    add_date = db.DateTimeProperty(auto_now_add=True)
    rate = db.FloatProperty(default=0.0)
    rate_count = db.IntegerProperty(default=0)
    rate_ips = db.StringListProperty(default=None)
    
    @classmethod
    def add(cls, user, name, category, link, pic, tags=''):
        blog = Blog(user=user, name=name, category=category, link=link, pic=pic)
        blog.tags = tags;
        blog.put()
    
    @classmethod
    def admin_add(cls, mail, name, category, link, pic, tags=''):
        Blog.add(db.users.User(mail) ,name, category, link, pic, tags)
        
    def update(self, name, category, link, tags):
        """更新博客信息，如果图片数据为空则不更新信息，否则更新图片信息"""
        self.name = name
        self.category = category
        self.link = link
        self.tags = tags
        self.put()
        
    def update_pic(self, pic):
        self.pic = db.Blob(pic)
        self.put()
        
    def add_rate(self, score, ip):
        """投票"""
        if ip in self.rate_ips:
            return {"success": False, "rate": self.rate, "rate_count": self.rate_count}
        self.rate_ips.append(ip)
        self.rate = (self.rate * self.rate_count + score) / (self.rate_count + 1)
        self.rate_count += 1
        self.put()
        
        return {"success": True, "rate": self.rate, "rate_count": self.rate_count}
    
class Feed(BaseModel):
    user = db.UserProperty(required=True)
    feed_url = db.StringProperty(required=True)
    title = db.StringProperty()
    subtitle = db.StringProperty()
    link = db.StringProperty()
    
    @classmethod
    def add(cls, user, url, title='', subtitle='', link=''):
        blog = Feed(user=user, feed_url=url)
        blog.title = title
        blog.subtitle = subtitle
        blog.link = link
        blog.put()

class Entry(BaseModel):
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
        if ip in self.rate_ips:
            return False
        self.rate_count += 1
        self.rate_ips.append(ip)
        self.put()
        return True
        
class Category(BaseModel):
    cateid = db.IntegerProperty()
    name = db.StringProperty()
    blog = db.ReferenceProperty(Blog)