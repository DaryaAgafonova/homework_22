from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at', 'views_count')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'image', 'author')
        }),
        ('Публикация', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
        ('Статистика', {
            'fields': ('views_count',)
        }),
    )