#coding=utf-8
#!/usr/bin/env python

import urllib
import json

def get_ticket():
    #获取access_token
    access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxd2a9d9dbc0333a47&secret=be8a0887afd1ec6c9e842b5d02b9d637"
    access_token_str = urllib.urlopen(access_token_url)
    access_token_dict = json.load(access_token_str)
    access_token = access_token_dict["access_token"]

    #获取jsApi_ticket
    ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=" + access_token + "&type=jsapi"
    tiket_str = urllib.urlopen(ticket_url)
    tiket_dict = json.load(tiket_str)
    ticket = tiket_dict["ticket"]
    #print ticket
    file = open("/home/github/django_blog/wechat/util/ticket.txt", 'wb+')
    file.write(ticket)
    file.close()

    return ticket


if __name__ == '__main__':
    get_ticket()
