# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.utils import simplejson

from google.appengine.api import users, images

from common import models
from common.taggable import Tag
from common.helper import requires_admin
from django.core.context_processors import request


def index(request):
    """博客秀首页。"""
    
    tags = Tag.all().fetch(limit=1000)
    
    template = loader.get_template('blogshow/templates/index.html')
    context = Context({
        "tags": tags,
    })
    
    return HttpResponse(template.render(context))

def bloglist(request):
    """博客列表。"""
    
    tagkey = request.GET.get('tagkey')
    if tagkey:
        taggeds = Tag.get(tagkey).tagged
        blogs = (models.Blog.get(tagged) for tagged in taggeds)
    else:
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

@requires_admin
def convert_category_to_tag(request):
    """批量将原来的category转换为tag。"""
    
    for blog in models.Blog.all().fetch(limit=1000):
        if blog.category == '1':
            blog.tags = u'快乐'
        elif blog.category == '2':
            blog.tags = u'技术'
        elif blog.category == '3':
            blog.tags = u'学习'
        elif blog.category == '4':
            blog.tags = u'生活'
        blog.put()
        
    return HttpResponse()

