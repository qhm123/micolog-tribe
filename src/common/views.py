# -*- coding: utf-8 -*

import logging

from django import template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import Context, loader
from django.core.urlresolvers import reverse

def common_404(request, template_name='404.html'):
    # You need to create a 404.html template.
    t = loader.get_template(template_name)
    return HttpResponseNotFound(
        t.render(template.RequestContext(request, {'request_path': request.path})))


def common_500(request, template_name='500.html'):
    logging.error("An error occurred: %s", str(request))
    # You need to create a 500.html template.
    t = loader.get_template(template_name)
    #  return http.HttpResponseServerError(
    #      t.render(template.RequestContext(request, {})))
    return HttpResponse(t.render(template.RequestContext(request, {})))
