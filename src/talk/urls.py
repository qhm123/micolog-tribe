# coding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('talk.views',
   (r'^$', 'index'),
   (r'^send$', 'send'),
   (r'^history$', 'history'),
   (r'^init_talkstatus$', 'init_talkstatus'),
   (r'^init_talkstatus_test$', 'init_talkstatus_test'),
)