# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('rssa.views',
    (r'^$', 'index'),
    (r'^rate', 'rate'),
    (r'^feed', 'feed'),
    (r'^add_all$', 'add_all'),
    (r'^fetch_feed$', 'fetch_feed'),
    (r'^fetch_feed_worker$', 'fetch_feed_worker'),
    (r'^refresh_db_feedentry', 'refresh_db_feedentry'),
)