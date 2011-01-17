# -*- coding: utf-8 -*

from datetime import tzinfo, timedelta, datetime

class UTC0(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=0)
    def tzname(self, dt):
        return "UTC +0"
    def dst(self,dt):
        return timedelta(0)

class UTC8(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=8)
    def tzname(self, dt):
        return "UTC +8"
    def dst(self,dt):
        return timedelta(0)
    
def to_utc8(date):
    dt = date + timedelta(hours=8)
    return dt.astimezone(UTC8())