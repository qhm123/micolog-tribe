# coding: utf-8

import logging

from google.appengine.api import xmpp

def test():
    user_addr = 'qhm123@gmail.com'
    if xmpp.get_presence(jid=user_addr):
        msg = 'Hello'
        status_code = xmpp.send_message(jids=user_addr, body=msg)
        if status_code == xmpp.NO_ERROR:
            logging.warning("send failed! msg: %s." % msg)
        
def recieve(request):
    if request.method == 'POST':
        message = xmpp.Message(request.POST)
        message.reply('Greetings!')
    
if __name__ == '__main__':
    test()