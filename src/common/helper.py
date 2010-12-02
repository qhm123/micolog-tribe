# -*- coding: utf-8 -*

from functools import wraps

from django.http import HttpResponse, HttpResponseRedirect

from google.appengine.api import users

def get_referer_url(request):
    """获得请求页的url"""
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/' # 避免外站直接跳到登录页而发生跳转错误
    return referer_url

def requires_admin(method):
    """需要管理员权限，否则什么也不做"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            return HttpResponseRedirect(users.create_login_url(get_referer_url(self.META["HTTP_HOST"] + self.path)))
        elif not users.is_current_user_admin():
            return HttpResponseRedirect(users.create_login_url(get_referer_url(self.META["HTTP_HOST"] + self.path)))
        else:
            return method(self, *args, **kwargs)
    return wrapper