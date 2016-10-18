from django.shortcuts import render

from .models import Blog

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def blog(request):
    blog_list = Blog.objects.order_by('-update_time')[:5]
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)