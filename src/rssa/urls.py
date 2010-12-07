# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('rssa.views',
    (r'^$', 'index'),
    (r'^add$', 'add'),
    (r'^add_all$', 'add_all'),
    (r'^fetch_feed$', 'fetch_feed'),
    (r'^refresh_db_feedentry', 'refresh_db_feedentry'),
    (r'^rate', 'rate'),
    (r'^feed', 'feed'),
)