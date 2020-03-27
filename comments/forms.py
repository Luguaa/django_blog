from django import forms
from .models import Comment


# 表单功能必须继承forms.Form或者forms.ModelForm类
class CommentForm(forms.ModelForm):
    class Meta:
        # 对应数据库Comment模型类
        model = Comment
        # 指定表单需要显示的字段
        fields = ['name', 'email', 'url', 'text']