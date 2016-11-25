from django.contrib import admin
from .models import Blog
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.
    

admin.site.register(Blog, MarkdownxModelAdmin)
