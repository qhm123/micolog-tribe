from appengine_django.models import BaseModel
from google.appengine.ext import db

class Tribe(BaseModel):
    manual = db.TextProperty(default='')
    
    @classmethod
    def getManual(cls):
        if Tribe.all().get() is None:
            tribe = Tribe()
            tribe.put()
        return Tribe.all().get().manual
