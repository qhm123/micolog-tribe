from appengine_django.models import BaseModel
from google.appengine.ext import db
from xmlrpclib import datetime

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
            entry.date = datetime.datetime(updated[0], updated[1], updated[2], updated[3], updated[4], updated[5])
            entry.description = description
            entry.content = content
            entry.feed = feed
            entry.put()