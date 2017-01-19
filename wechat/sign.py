import time
import random
import string
import hashlib

class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

if __name__ == '__main__':
    sign = Sign('kgt8ON7yVITDhtdwci0qeTWQwsqkmCCxl3Cird9AlCRs-cuzQpahA3T-srqrnXAP2zuxETCtM-um_xIiylWedg', 'http://zhouyafeng.cn/wechat/')
    print sign.sign()
