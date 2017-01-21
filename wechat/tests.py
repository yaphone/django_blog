from django.test import TestCase

file = open("./util/ticket.txt")
ticket = file.read()
print ticket
