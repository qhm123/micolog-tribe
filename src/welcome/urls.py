# -*- coding: utf-8 -*

from django.conf.urls.defaults import *

urlpatterns = patterns('welcome.views',
    (r'^$', 'index'),
    (r'^gtalk', 'gtalk'),
    (r'^about$', 'about'),
)