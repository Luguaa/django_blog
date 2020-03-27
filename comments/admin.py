from django.contrib import admin
from .models import Comment


# Register your models here.
class CommentaAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'post', 'create_time']
    fields = ['name', 'email', 'url', 'text', 'post']


admin.site.register(Comment, CommentaAdmin)
