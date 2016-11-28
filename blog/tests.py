from django.test import TestCase

# Create your tests here.
for i in range(10):
    if i % 2 == 0:
        continue
    print i