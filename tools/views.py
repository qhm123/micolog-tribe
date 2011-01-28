# coding: utf-8

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

from django import http
from django.template import RequestContext, loader

from common.models import Blog
import logging

IP = '203.208.39.104'

def hosts(request):
    
    links = (blog.link[7:].encode('utf8').split('/')[0] for blog in Blog.all().fetch(limit=1000) if 'appspot.com' in blog.link)
    
    template = loader.get_template('tools/templates/hosts.html')
    context = RequestContext(request, {
        'links': links,
        'ip': IP,
    })
    
    return http.HttpResponse(template.render(context))

def rpc_handler(request):
    
    if len(request.POST):
        response = http.HttpResponse(mimetype="application/xml")
        response.write(server._marshaled_dispatch(request.raw_post_data))
    else:
        response = http.HttpResponse()
        response.write("<b>This is an XML-RPC Service.</b><br>")
        response.write("You need to invoke it using an XML-RPC Client!<br>")
        
#        response.write("The following methods are available:<ul>")
#        methods = server.system_listMethods()
#
#        for method in methods:
#            # right now, my version of SimpleXMLRPCDispatcher always
#            # returns "signatures not supported"... :(
#            # but, in an ideal world it will tell users what args are expected
#            sig = server.system_methodSignature(method)
#
#            # this just reads your docblock, so fill it in!
##            help =  server.system_methodHelp(method)
#            help = ''
#
#            response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))
#
#        response.write("</ul>")
#        response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')
#
#    response['Content-length'] = str(len(response.content))
    return response

server = SimpleXMLRPCDispatcher()
server.register_introspection_functions()
        
def ping(name, site_url, entry_url, rss_url):
    logging.info('ping %s %s %s %s' % (name, site_url, entry_url, rss_url))
    return 'ping %s %s %s %s' % (name, site_url, entry_url, rss_url)

server.register_function(ping, 'weblogUpdates.ping')

