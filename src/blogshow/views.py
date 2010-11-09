# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

def index(request):
    template = loader.get_template('index.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))