from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType

# Create your views here.
# 博客列表页
def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blog_list.html', context)

# 博客详情页
def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog/blog_detail.html', context)

# 根据分类查询博客
def blogs_with_type(request, blogs_with_type):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blogs_with_type)
    context['blog_type'] = blog_type
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blogs_with_type.html', context)