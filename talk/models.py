# coding: utf-8

from appengine_django.models import BaseModel
from google.appengine.ext import db

from common.models import Blog

class TalkLog(BaseModel):
    """消息记录模型。"""
    
    user = db.UserProperty()
    msg = db.StringProperty()
    time = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def add(cls, user, msg):
        log = TalkLog(user=user, msg=msg)
        log.put()

class TalkStatus(BaseModel):
    """聊天状态信息"""
    
    user = db.UserProperty()
    online = db.BooleanProperty(default=False)
    nickname = db.StringProperty()
    msg_count = db.IntegerProperty(default=0)
    blog = db.ReferenceProperty(Blog)
    
    @classmethod
    def add(cls, user, blog):
        status = TalkStatus(user=user, blog=blog)
        status.put()