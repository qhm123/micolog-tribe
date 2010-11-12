# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from google.appengine.api import users

import models

def index(request):
    template = loader.get_template('welcome/templates/index.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))