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
        self.updated = updated
        self.description = description
        self.content = content