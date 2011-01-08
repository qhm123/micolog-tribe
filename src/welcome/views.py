# -*- coding: utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse

from google.appengine.api import users, images

from common import models
from common.helper import requires_admin

def index(request): 
    
    template = loader.get_template('welcome/templates/index.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))

def about(request):
    manual = models.Tribe.getManual()
    
    template = loader.get_template('welcome/templates/about.html')
    context = Context({
        'manual': manual,
    })
    
    return HttpResponse(template.render(context))

def gtalk(request):  
    template = loader.get_template('welcome/templates/chat.html')
    context = Context({
    })
    
    return HttpResponse(template.render(context))

def add(request):
    """添加一个博客。"""
    
    if request.method == 'GET':
        user = users.get_current_user()
        if not user:
            login_url = users.create_login_url(reverse('blogshow.views.add'))
            return HttpResponseRedirect(login_url)
        blog = models.Blog.all().filter('user =', user).get()
        
        template = loader.get_template('welcome/templates/add.html')
        context = Context({
            "blog": blog,
            'showmail': False,
        })
        
        return HttpResponse(template.render(context))
    else:
        user = users.get_current_user()
        if user:
            name = request.POST.get('name', '')
            # TODO: 去掉category
            category = "1"
            link = request.POST.get('link', '')
            if 'http://' not in link:
                link = 'http://' + link
            pic = request.FILES.get('file')
            tags = request.POST.get('tags')
            feedurl = request.POST.get('feedurl')
            tt = tags.encode('utf8')
            
            blog = models.Blog.all().filter('user =', user).get()
            
            # 如果当前用户博客为空，且图片不为空，则添加博客上传图片
            if not blog and pic:
                pic = images.resize(pic.read(), 190, 130)
                models.Blog.add(user, name, category, link, pic, tags, feedurl)
            # 如果当前用户博客不为空，则更新博客信息
            elif blog:
                blog.update(name, category, link, tags, feedurl)
                if pic:
                    pic = images.resize(pic.read(), 190, 130)
                    blog.update_pic(pic)
            
        return HttpResponseRedirect(reverse('welcome.views.add'))

def deal_link(link):
    if not link.startswith('http://'):
        link = 'http://' + link
        
    return link

@requires_admin
def admin_add(request):
    """管理员专用：管理员添加博客。"""
    
    if request.method == 'GET':
        template = loader.get_template('welcome/templates/add.html')
        context = Context({
            'showmail': True,
        })
        
        return HttpResponse(template.render(context))
    else:
        name = request.POST.get('name', '')
        mail = request.POST.get('mail', '')
        # TODO: 去掉category
        category = "1"
        link = request.POST.get('link', '')
        if 'http://' not in link:
            link = 'http://' + link
        pic = request.FILES.get('file')
        tags = request.POST.get('tags')
        feedurl = request.POST.get('feedurl')
        
        # 如果当前用户博客为空，且图片不为空，则添加博客上传图片
        pic = images.resize(pic.read(), 190, 130)
        models.Blog.admin_add(mail, name, category, link, pic, tags, feedurl)
            
        return HttpResponseRedirect(reverse('welcome.views.admin_add'))