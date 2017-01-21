#!/usr/bin/env python
from django.test import TestCase

import time

def test():
    file = open("/home/github/django_blog/wechat/util/test.txt", 'wb+')
    file.write("123")
    file.close()

if __name__ == '__main__':
    test()


