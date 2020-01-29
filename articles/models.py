from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

from core.models import TimestampedModel

alphanumeric = RegexValidator(r'^[0-9a-zA-Z\-\s]*$', 'Only alphanumeric characters, hyphen are allowed.')


class Article(TimestampedModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    tag = models.ManyToManyField('Tag')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + '...'


class Tag(TimestampedModel):
    title = models.CharField(max_length=50, unique=True, validators=[alphanumeric])

    def __str__(self):
        return self.title.lower().replace(' ', '-')
