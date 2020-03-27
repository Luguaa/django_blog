from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags

import markdown

# Create your models here.
class Category(models.Model):
    '''分类'''
    name = models.CharField(max_length=100)

    # 后台管理页面显示中文
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    # 命令行时返回name
    def __str__(self):
        return self.name


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=100)

    # 后台管理页面显示中文
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    # 命令行时返回name
    def __str__(self):
        return self.name


class Post(models.Model):
    '''文章'''

    # 文章标题
    title = models.CharField('标题', max_length=70)

    # 文章正文
    # TextField用来存储大段文本
    body = models.TextField('正文')

    # 文章的创建时间和最后一次修改时间
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要（可以没有）
    # blank=True:允许文章摘要为空
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 分类：一个分类可以有多个文章，一对多
    # 标签：一个文章可以有多个标签，多对多，允许没有标签
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 作者，从django.contrib.auth.models导入，一对多
    # django.contrib.auth:Django自带的用户模型
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    # 后台管理页面显示中文
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    # 命令行时返回name
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 重写save方法，在save时将修改时间设定为当前时间
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite'
        ])
        # strip_tags 去掉HTML文本的全部HTML标签
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)