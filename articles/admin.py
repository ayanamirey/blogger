from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article, Tag

admin.site.register(Article, MarkdownxModelAdmin)
admin.site.register(Tag)
