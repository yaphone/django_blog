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
    reading_count = models.IntegerField(default=0)
    music = models.CharField(max_length=300, default="null")


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    nickname = models.TextField(max_length=20)
    comment_time = models.DateTimeField()
    email = models.CharField(max_length=100)
    content = models.TextField(max_length = 2000)

class SubComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    nickname = models.TextField(max_length=20)
    comment_time = models.DateTimeField()
    email = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)