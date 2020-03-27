from django.shortcuts import render, get_object_or_404, redirect
# 支持处理中文
from django.utils.text import slugify
from .models import Post, Category, Tag

import markdown, re
from markdown.extensions.toc import TocExtension


# Create your views here.
def index(request):

    post_list = Post.objects.all().order_by('-create_time')

    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    '''详情页'''
    post = get_object_or_404(Post, pk=pk)
    # 添加markdown支持
    # extra:对markdown语法的拓展
    # codehilite:语法高亮拓展
    # toc:允许自动生成目录
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        # 美化锚点
        TocExtension(slugify=slugify)
    ])
    # 解析成html
    post.body = md.convert(post.body)

    # 添加toc属性, 当没有目录时显示为空
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    '''归档视图'''
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month,
                                    ).order_by('-create_time')

    return render(request, 'blog/index.html', context={'post_list':post_list})


def category(request, pk):
    '''侧边栏分类视图'''
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    '''侧边栏标签'''
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})
