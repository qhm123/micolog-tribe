# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('blogshow.views',
    (r'^', 'index'),
)