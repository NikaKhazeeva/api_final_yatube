from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Group, Post, Comment, Follow

User = get_user_model()


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author', 'group', 'image')
    list_filter = ('pub_date', 'author', 'group')
    search_fields = ('text', 'author__username', 'group__title')
    date_hierarchy = 'pub_date'
    raw_id_fields = ('author', 'group')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created')
    list_filter = ('created', 'author', 'post')
    search_fields = ('text', 'author__username', 'post__text')
    date_hierarchy = 'created'
    raw_id_fields = ('author', 'post')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    list_filter = ('user', 'following')
    search_fields = ('user__username', 'following__username')
    raw_id_fields = ('user', 'following')
