# coding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('tools.views',
    (r'^hosts$', 'hosts'),
)
