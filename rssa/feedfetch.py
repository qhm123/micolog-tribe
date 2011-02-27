# coding: utf-8

from datetime import datetime

import feedparser


class FeedParser():
    
    def __init__(self, url):
        self.fetch(url)
    
    def fetch(self, url):
        feed = feedparser.parse(url)
        self.title = feed.channel.title
        self.subtitle = feed.channel.subtitle
        self.link = feed.channel.link
        self.entries = (Entry(entry.id,
                              entry.title,
                              entry.link,
                              entry.updated,
                              entry.description,
                              entry.content[0].value) for entry in feed.entries)
            
class Entry():
    
    def __init__(self, id, title, link, updated, description, content):
        self.id = id;
        self.title = title
        self.link = link
        #Tue, 09 Nov 2010 08:33:11 +0000
        self.updated = datetime.strptime(updated, '%a, %d %b %Y %H:%M:%S +0000')
        self.description = description
        self.content = content
        
if __name__ == "__main__":
    feed = FeedParser("http://www.qhm123.com/feed")
    print feed.title
    print feed.subtitle
    print feed.link
    print feed.entries
    for entry in feed.entries:
        print entry.id
        print entry.title
        print entry.link
        print entry.updated
        print entry.description
        print entry.content
    