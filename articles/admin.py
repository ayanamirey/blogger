from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from modeltranslation.admin import TranslationAdmin

from .models import Article, Tag, Comment, Category, LikeOfArticle, FavouriteArticles, ReportToComment, ReportToArticle

# admin.site.register(LikeOfArticle)
admin.site.register(Tag)


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


@admin.register(FavouriteArticles)
class FavouriteArticlesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')


@admin.register(ReportToComment)
class ReportToCommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')


@admin.register(ReportToArticle)
class ReportToArticleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')


@admin.register(Category)
class ReportToArticleAdmin(TranslationAdmin):
    list_display = ('__str__', 'id', 'title_uz', 'menu_position')
