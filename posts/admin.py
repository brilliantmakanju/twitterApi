from django.contrib import admin
from .models import Profile, PostImage, Post, Comment, Reply
# Register your models here.

admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(PostImage)