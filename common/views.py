# -*- coding: utf-8 -*

import logging

from django import template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import Context, loader
from django.core.urlresolvers import reverse

def common_404(request):
    template = loader.get_template('common/templates/404.html')
    context = Context({})
    return HttpResponseNotFound(template.render(context))

def common_500(request):
    logging.error("An error occurred: %s", str(request))

    template = loader.get_template('common/templates/500.html')
    context = Context({})
    return HttpResponse(template.render(context))
