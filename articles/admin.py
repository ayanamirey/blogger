from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article, Tag, Comment, Category, LikeOfArticle

# admin.site.register(LikeOfArticle)
admin.site.register(Tag)
admin.site.register(Category)


@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin):
    list_display = ('__str__', 'author', 'status', )
    list_editable = ('status', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'parent', 'status', 'id')
    list_editable = ('status', )
    readonly_fields = ('id', 'content')


@admin.register(LikeOfArticle)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')

