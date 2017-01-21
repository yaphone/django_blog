#!/usr/bin/env python
from django.test import TestCase

import time

def test():
    file = open("./util/test.txt", 'a+')
    file.write("123")
    file.close()

if __name__ == '__main__':
    test()


