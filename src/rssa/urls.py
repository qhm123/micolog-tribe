# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('rssa.views',
    (r'^$', 'index'),
)