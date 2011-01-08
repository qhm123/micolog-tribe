# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.utils import simplejson

from google.appengine.api import users, images

from common import models
from common.helper import requires_admin


def index(request):
    # TODO: 考虑重构，现在有点恶心……
    cate_count = [models.Blog.all().filter('category =', str(cateid)).count(limit=1000) for cateid in range(1, 5)]
    
    template = loader.get_template('blogshow/templates/index.html')
    context = Context({
        "happy_count": cate_count[0],
        "tech_count": cate_count[1],
        "study_count": cate_count[2],
        "life_count": cate_count[3],
    })
    
    return HttpResponse(template.render(context))

def add(request):
    if request.method == 'GET':
        user = users.get_current_user()
        if not user:
            login_url = users.create_login_url(reverse('blogshow.views.add'))
            return HttpResponseRedirect(login_url)
        blog = models.Blog.all().filter('user =', user).get()
        
        template = loader.get_template('blogshow/templates/add.html')
        context = Context({
            "blog": blog,
            'showmail': False,
        })
        
        return HttpResponse(template.render(context))
    else:
        user = users.get_current_user()
        if user:
            name = request.POST.get('name', '')
            category = request.POST.get('category', '')
            link = request.POST.get('link', '')
            if 'http://' not in link:
                link = 'http://' + link
            pic = request.FILES.get('file')
            tags = ''
            
            blog = models.Blog.all().filter('user =', user).get()
            
            # 如果当前用户博客为空，且图片不为空，则添加博客上传图片
            if not blog and pic:
                pic = images.resize(pic.read(), 190, 130)
                models.Blog.add(user, name, category, link, pic)
            # 如果当前用户博客不为空，则更新博客信息
            elif blog:
                blog.update(name, category, link, tags)
                if pic:
                    pic = images.resize(pic.read(), 190, 130)
                    blog.update_pic(pic)
            
        return HttpResponseRedirect(reverse('blogshow.views.add'))

@requires_admin
def admin_add(request):
    if request.method == 'GET':
        template = loader.get_template('blogshow/templates/add.html')
        context = Context({
            'showmail': True,
        })
        
        return HttpResponse(template.render(context))
    else:
        name = request.POST.get('name', '')
        mail = request.POST.get('mail', '')
        category = request.POST.get('category', '')
        link = request.POST.get('link', '')
        if 'http://' not in link:
            link = 'http://' + link
        pic = request.FILES.get('file')
        tags = ''
        
        # 如果当前用户博客为空，且图片不为空，则添加博客上传图片
        pic = images.resize(pic.read(), 190, 130)
        models.Blog.admin_add(mail, name, category, link, pic)
            
        return HttpResponseRedirect(reverse('blogshow.views.admin_add')) 
    
def rate(request):
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

def bloglist(request):
    cateid = request.GET.get('cateid')
    blogs = models.Blog.all().filter('category =', cateid).order('-rate').order('-rate_count').order('add_date').fetch(limit=1000)
    
    template = loader.get_template('bloglist.html')
    context = Context({
        'blogs': blogs,
    })
    
    return HttpResponse(template.render(context))

@requires_admin
def refresh_db_blog(request):
    for blog in models.Blog.all().fetch(limit=1000):
        blog.rate = 0.0
        blog.rate_count = 0
        blog.rate_ips = []
        blog.put()
    return HttpResponse()

def img(request, blog_id):
    blog = models.Blog.get_by_id(int(blog_id))
    if blog.pic:
        #request.POST.headers['Content-Type'] = "image/jepg"
        response = HttpResponse(blog.pic, content_type="image/png")
        response['Expires'] = 'Thu, 15 Apr 3010 20:00:00 GMT'
        response['Cache-Control'] = 'max-age=36000,public'
        return response
    else:
        return HttpResponse(blog.pic)