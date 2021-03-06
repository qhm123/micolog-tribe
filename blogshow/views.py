# -*- coding: utf-8 -*

from django.http import HttpResponse
from django.template import loader, RequestContext
from django.utils import simplejson
from django.conf import settings

from google.appengine.api import memcache, mail
from google.appengine.ext import db

from common import models
from common.taggable import Tag
from common.helper import requires_admin

def index(request):
    """博客秀首页。"""
    
    tags = Tag.all().filter('isshow', True).filter('tagged_count >', 1).fetch(limit=1000)
    
    template = loader.get_template('blogshow/templates/index.html')
    context = RequestContext(request, {
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
    context = RequestContext(request, {
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
        voter = u'有人'
        user = db.users.get_current_user()
        if user:
            vote_blog = models.Blog.all().filter('user =', user).get()
            if vote_blog:
                voter = '%s|%s' % (user, vote_blog.name)
                voter_link = vote_blog.link
            else:
                voter = '%s|%s' % (user, 'blog')
                voter_link = "http://micolog-tribe.qhm123.com"
        else:
            voter_link = '#'
        
        to = blog.user.email()
        subject = u'有人给您的博客投票了，快去看看。'
        html = u'''您在<a href="http://micolog-tribe.qhm123.com" target="_blank">Micolog部落</a>上注册的博客：<a href="%s" target="_blank">%s</a>。<br/>
<a href="%s" target="_blank">%s</a>给您的博客投票了，快去<a href="http://micolog-tribe.qhm123.com/blogshow" target="_blank">看看</a>。<br/>
您也可以给别人的博客投票，<a href="http://micolog-tribe.qhm123.com/blogshow" target="_blank">试试看</a>。<br/>
''' % (blog.link, blog.name, voter_link, voter)
        mail.send_mail(settings.MAILSENDER, to, subject, u"body", html=html)
        return HttpResponse(simplejson.dumps({"success": True, "rate": rate['rate'], "rate_count": rate['rate_count'], "blogid": blogid}), mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps({"success": False, "rate": rate['rate'], "rate_count": rate['rate_count'], "blogid": blogid}), mimetype='application/json')

def img(request, blog_id):
    """img请求应答函数。"""
    
    pic = memcache.get(key='pic-%s' % blog_id)
    if pic is None:
        blog = models.Blog.get_by_id(int(blog_id))
        pic = blog.pic
        memcache.add(key='pic-%s' % blog_id, value=pic)

    response = HttpResponse(pic, content_type="image/png")
    response['Expires'] = 'Thu, 15 Apr 3010 20:00:00 GMT'
    response['Cache-Control'] = 'max-age=36000,public'
    return response
    
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
def refresh_blog_rateips(request):
    
    for blog in models.Blog.all().fetch(limit=1000):
        blog.rate_ips = []
        blog.put()
    return HttpResponse()

@requires_admin
def refresh_blog_isshow_property(request):
    
    for blog in models.Blog.all().fetch(limit=1000):
        blog.isshow = True
        blog.put()
    return HttpResponse()

@requires_admin
def convert_category_to_tag(request):
    """批量将原来的category转换为tag。"""
    
    for blog in models.Blog.all().fetch(limit=1000):
        if blog.tags is None or len(blog.tags) == 0:
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

