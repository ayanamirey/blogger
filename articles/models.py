from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from markdownx.models import MarkdownxField
import re

from markdownx.utils import markdownify

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
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    @property
    def formatted_markdown(self):
        return strip_tags(markdownify(self.body))

    def snippet(self):
        return self.formatted_markdown[:150].replace('\n', ' ') + '...'

    def snippet_large(self):
        return self.formatted_markdown[:350].replace('\n', ' ') + '...'

    def time_of_read(self):
        t1 = len(self.formatted_markdown.replace('\n', '')) / 1500
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

    def get_comments(self):
        return self.comment_set.filter(parent__isnull=True)

    def count_of_likes(self):
        return LikeOfArticle.objects.filter(article_id=self.id).count()

    def count_of_comments(self):
        return Comment.objects.filter(article_id=self.id).count()

    def count_of_favourites(self):
        return FavouriteArticles.objects.filter(article_id=self.id).count()


class Comment(TimestampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25,
                              choices=(('active', 'ACTIVE'), ('deleted', 'DELETED')),
                              default='active')

    def __str__(self):
        return self.content[0:200]


class Category(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    menu_position = models.PositiveSmallIntegerField(default=0)  # if 0, not position. Status = False
    image = models.ImageField(upload_to='categories/', blank=True, null=True)


class LikeOfArticle(models.Model):
    article = models.OneToOneField('Article', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.article.title}-{self.user.username} [{self.id}]'


class FavouriteArticles(models.Model):
    article = models.OneToOneField('Article', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.article.title}-{self.user.username} [{self.id}]'

    def save(self, *args, **kwargs):
        if FavouriteArticles.objects.filter(article=self.article, user=self.user).count() == 0:
            super(FavouriteArticles, self).save(*args, **kwargs)
        else:
            pass
