from django.contrib.auth.models import User
from django.db import models

from articles.models import Category


class FollowToUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserOfUser')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='TargetOfUser')
    following_date = models.DateTimeField(auto_now_add=True)


class FollowToCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserOfCategory')
    target = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='TargetOfCategory')
    following_date = models.DateTimeField(auto_now_add=True)
