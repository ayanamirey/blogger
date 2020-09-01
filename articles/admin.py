from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article, Tag, Comment

admin.site.register(Article, MarkdownxModelAdmin)
admin.site.register(Tag)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'parent', 'status', 'id')
    list_editable = ('status', )
    readonly_fields = ('id', 'content')
