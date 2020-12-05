from django import forms
from markdownx.fields import MarkdownxFormField

from . import models
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^([0-9a-zA-Z\-\s]*[,]){,4}[0-9a-zA-Z\-\s]*$',
                              'Only alphanumeric characters, hyphen are allowed. Maximum 5 tags can be used')


class CreateArticle(forms.ModelForm):
    tag = forms.CharField(max_length=100, validators=[alphanumeric], help_text='(Separate tags with comma)')

    class Meta:
        model = models.Article
        fields = ['title', 'body', 'slug', 'category', 'tag']


class EditArticle(forms.ModelForm):
    tag = forms.CharField(max_length=100, validators=[alphanumeric], help_text='(Separate tags with comma)')
    body = MarkdownxFormField()

    class Meta:
        model = models.Article
        fields = ['title', 'body', 'slug', 'tag']


class CommentForms(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content', ]

    content = forms.CharField(
        widget=forms.Textarea(attrs={'required': True, 'style': 'resize: vertical; min-height: 160px; height: 200px'}),
        error_messages='', label='Content')
