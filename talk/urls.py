# coding: utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('talk.views',
   (r'^$', 'index'),
   (r'^send$', 'send'),
   (r'^online$', 'online'),
   (r'^offline$', 'offline'),
   (r'^history$', 'history'),
   (r'^online_list$', 'online_list'),
   (r'^invite_user_test$', 'invite_user_test'),
   (r'^invite_all_users$', 'invite_all_users'),
   (r'^init_talkstatus$', 'init_talkstatus'),
   (r'^init_talkstatus_test$', 'init_talkstatus_test'),
)