# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(max_length=128)),
                ('blog_content', models.TextField(max_length=1000000)),
                ('update_time', models.DateTimeField()),
                ('modify_time', models.DateTimeField()),
                ('blog_type', models.CharField(max_length=128)),
                ('blog_tag', models.CharField(max_length=128)),
            ],
        ),
    ]
