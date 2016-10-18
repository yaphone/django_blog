from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Blog(models.Model):
    blog_title = models.CharField(max_length = 128)
    blog_content = models.TextField(max_length=1000000)
    update_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    blog_type = models.CharField(max_length = 128)
    blog_tag = models.CharField(max_length = 128)