# coding: utf-8

import logging

from google.appengine.api import xmpp
from google.appengine.ext import db

import models as talk_models

def send(msg, sender=None):
    """群发消息。现在都返回成功。
    
    args: sender是Email地址。使用sender去除发送者。
    """
    
    if sender:
        user = db.users.User(email=sender)
    else:
        user = db.users.User(email='web@web.com')
    talk_models.TalkLog.add(user, msg)
    
    users = talk_models.TalkStatus.all().fetch(limit=1000)
    jids = [user.user.email() for user in users if user.user.email() != sender]
#    if talk.get_presence(jid=jid):
    status_codes = xmpp.send_message(jids=jids, body=msg)
#    for code in status_codes:
#        if status_codes == talk.NO_ERROR:
#            logging.warning("send failed! msg: %s." % msg)
#            return False
    return True
        
def recieve():
    pass
    
if __name__ == '__main__':
    send()