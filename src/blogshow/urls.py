# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('blogshow.views',
    (r'^$', 'index'),
    (r'^add$', 'add'),
    (r'^admin_add$', 'admin_add'),
    (r'^img/(?P<blog_id>\d+)$', 'img'),
    (r'^bloglist$', 'bloglist'),
    (r'^rate', 'rate'),
    (r'^refresh_db_blog', 'refresh_db_blog'),
)