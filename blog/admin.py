from django.contrib import admin
from .models import Category, Post, Tag


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    # 列表页面增加显示信息
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']

    # 表单页面修改显示信息，自动填写create_time, modified_time和user
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    # 自动填写user
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)