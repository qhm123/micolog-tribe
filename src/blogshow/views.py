# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from google.appengine.api import users, images

import models


def index(request):
    template = loader.get_template('index.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))

def add(request):
    if request.method == 'GET':
        user = users.get_current_user()
        if not user:
            login_url = users.create_login_url(reverse('blogshow.views.add'))
            return HttpResponseRedirect(login_url)
        blog = models.Blog.all().filter('user =', user).get()
        
        template = loader.get_template('add.html')
        context = Context({
            "blog": blog,
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

def bloglist(request):
    cateid = request.GET.get('cateid')
    blogs = models.Blog.all().filter('category =', cateid).order('add_date').fetch(limit=1000)
    
    template = loader.get_template('bloglist.html')
    context = Context({
        'blogs': blogs,
    })
    
    return HttpResponse(template.render(context))

def img(request, blog_id):
    blog = models.Blog.get_by_id(int(blog_id))
    if blog.pic:
        #request.POST.headers['Content-Type'] = "image/jepg"
        return HttpResponse(blog.pic, content_type="image/jepg")
    else:
        return HttpResponse(blog.pic)