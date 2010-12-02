# -*- coding: utf-8 -*

import urllib, hashlib

def get_avatar_url(email):
    try:
        avatar_url = "http://www.gravatar.com/avatar/"
        avatar_url += hashlib.md5(email.lower()).hexdigest() + "?" + \
            urllib.urlencode({'d': 'identicon',
                              's': '50',
                              'r': 'G'})
        return avatar_url
    except:
        return '/static/images/homsar.jpeg'