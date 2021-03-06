# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('blogshow.views',
    (r'^$', 'index'),
    (r'^img/(?P<blog_id>\d+)$', 'img'),
    (r'^bloglist$', 'bloglist'),
    (r'^rate', 'rate'),
    (r'^refresh_db_blog', 'refresh_db_blog'),
    (r'^convert_category_to_tag', 'convert_category_to_tag'),
    (r'^refresh_blog_rateips$', 'refresh_blog_rateips'),
    (r'^refresh_blog_isshow_property$', 'refresh_blog_isshow_property'),
)