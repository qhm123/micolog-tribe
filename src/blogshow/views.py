# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.utils import simplejson

from google.appengine.api import users, images

from common import models
from common.helper import requires_admin


def index(request):
    """博客秀首页。"""
    
    template = loader.get_template('blogshow/templates/index.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))

def bloglist(request):
    """博客列表。"""
    
    blogs = models.Blog.all().order('-rate').order('-rate_count').order('add_date').fetch(limit=1000)
    
    template = loader.get_template('bloglist.html')
    context = Context({
        'blogs': blogs,
    })
    
    return HttpResponse(template.render(context))
    
def rate(request):
    """给博客投票。"""
    
    blogid = request.POST.get('blogid')
    if blogid is None:
        return HttpResponse(status=400)
    score = request.POST.get('score')
    if score is None:
        return HttpResponse(status=400)
    ip = request.META['REMOTE_ADDR']
    blog = models.Blog.get_by_id(int(blogid))
    if blog is None:
        return HttpResponse(status=400)
    rate = blog.add_rate(int(score), ip)
    if rate["success"]:
        return HttpResponse(simplejson.dumps({"success": True, "rate": rate['rate'], "rate_count": rate['rate_count'], "blogid": blogid}), mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps({"success": False, "rate": rate['rate'], "rate_count": rate['rate_count'], "blogid": blogid}), mimetype='application/json')

def img(request, blog_id):
    """img请求应答函数。"""
    
    blog = models.Blog.get_by_id(int(blog_id))
    if blog.pic:
        #request.POST.headers['Content-Type'] = "image/jepg"
        response = HttpResponse(blog.pic, content_type="image/png")
        response['Expires'] = 'Thu, 15 Apr 3010 20:00:00 GMT'
        response['Cache-Control'] = 'max-age=36000,public'
        return response
    else:
        return HttpResponse(blog.pic)
    
@requires_admin
def refresh_db_blog(request):
    """慎用！管理员专用，更新Blog所有实体的投票数和投票IP列表。"""
    
    for blog in models.Blog.all().fetch(limit=1000):
        blog.rate = 0.0
        blog.rate_count = 0
        blog.rate_ips = []
        blog.put()
    return HttpResponse()