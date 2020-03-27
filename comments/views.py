from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import CommentForm

# Create your views here.
@require_POST
def comment(request, post_pk):
    # 获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    # 获取用户提交的表单
    form = CommentForm(request.POST)

    # 检查表单数据是否符合格式
    if form.is_valid():

        # 不保存到数据库
        comment = form.save(commit=False)

        # 评论关联文章
        comment.post = post

        # 保存到数据库
        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        return redirect(post)

    context = {
        'post': post,
        'form': form,
    }

    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交', extra_tags='danger')

    return render(request, 'comments/preview.html', context=context)

