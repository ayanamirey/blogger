from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
import re

from core.models import TimestampedModel

alphanumeric = RegexValidator(r'^[0-9a-zA-Z\-\s]*$', 'Only alphanumeric characters, hyphen are allowed.')


class Tag(TimestampedModel):
    title = models.CharField(max_length=50, unique=True, validators=[alphanumeric])

    def __str__(self):
        return self.title.lower().replace(' ', '-')


class Article(TimestampedModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    body = MarkdownxField()
    tag = models.ManyToManyField(Tag, related_name="articles")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    status = models.CharField(max_length=25,
                              choices=(('draft', 'DRAFT'), ('inreview', 'INREVIEW'), ('published', 'PUBLISHED')),
                              default='draft')

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:150] + '...'

    def snippet_large(self):
        return self.body[:350] + '...'

    def time_of_read(self):
        t1 = len(self.body) / 1500
        t2 = len([m.start() for m in re.finditer(r"(?:!\[(.*?)\]\((.*?)\))", self.body)])
        the_sum = t1 + t2
        n = int(the_sum * 10) % 10
        if the_sum < 1:
            result = '1'
        else:
            if n >= 3:
                result = str(int(the_sum) + 1)
            else:
                result = str(the_sum)
        return result + ' min'
