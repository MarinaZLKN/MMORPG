from django.contrib import admin
from .models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text')

@admin.register(Post)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datecreation', )
