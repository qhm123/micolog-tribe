# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('welcome.views',
    (r'^$', 'index'),
    (r'^about$', 'about'),
    (r'^add$', 'add'),
    (r'^admin_add$', 'admin_add'),
    (r'^refresh_tags$', 'refresh_tags'),
    (r'^refresh_tags_worker$', 'refresh_tags_worker'),
)