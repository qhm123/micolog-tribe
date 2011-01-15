# coding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('talk.views',
   (r'^$', 'index'),
   (r'^send$', 'send'),
)