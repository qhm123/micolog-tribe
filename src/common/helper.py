# -*- coding: utf-8 -*

from functools import wraps

from google.appengine.api import users

def requires_admin(method):
    """需要管理员权限，否则什么也不做"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            return
        elif not users.is_current_user_admin():
            return
        else:
            return method(self, *args, **kwargs)
    return wrapper