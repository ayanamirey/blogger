from modeltranslation.translator import TranslationOptions, register

from articles.models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
