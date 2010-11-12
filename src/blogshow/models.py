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
    
    @classmethod
    def add(cls, user, name, category, link, pic, tags=''):
        blog = Blog(user=user, name=name, category=category, link=link, pic=pic)
        blog.tags = tags;
        blog.put()
        
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
        
class Category(BaseModel):
    cateid = db.IntegerProperty()
    name = db.StringProperty()
    blog = db.ReferenceProperty(Blog)