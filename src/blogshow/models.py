# -*- coding: utf-8 -*

from appengine_django.models import BaseModel
from google.appengine.ext import db

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
        
class Category(BaseModel):
    cateid = db.IntegerProperty()
    name = db.StringProperty()
    blog = db.ReferenceProperty(Blog)