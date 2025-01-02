from django.contrib import admin
from .models import Tag, Product, Picture, Comment, Like

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'location', 'created_at')
    list_filter = ('label', 'tags')
    search_fields = ('name', 'description')
    filter_horizontal = ('tags',)

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'text', 'created_at', 'like_count')
    list_filter = ('created_at',)
    search_fields = ('text',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    list_filter = ('created_at',)
