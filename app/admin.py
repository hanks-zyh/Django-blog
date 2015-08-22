from django.contrib import admin
from models import User, Article, Comment, Tag, Category, Links, Ad


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend', 'tag', 'category',)
        }),
    )


admin.site.register(User)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Links)
admin.site.register(Ad)
