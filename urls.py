# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^smedia/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),    
)

urlpatterns += patterns('',
    (r'^', include('welcome.urls')),
    (r'^blogshow/', include('blogshow.urls')),
    (r'^rssa/', include('rssa.urls')),
    (r'^talk/', include('talk.urls')),
    (r'^_ah/xmpp/message/chat/', 'talk.views.recieve'),
    (r'^tools/', include('tools.urls')),
)

handler404 = 'common.views.common_404'
handler500 = 'common.views.common_500'
