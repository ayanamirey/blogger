from django import template

from accounts.models import FollowToCategory, FollowToUsers
from articles.models import Category

register = template.Library()


@register.simple_tag
def get_active_categories():
    return Category.get_active_categories()


@register.simple_tag
def is_followed(cat_id, user_id):
    return FollowToCategory.objects.filter(target_id=cat_id, user_id=user_id).exists()


@register.simple_tag
def is_user_followed(target_id, user_id):
    return FollowToUsers.objects.filter(target_id=target_id, user_id=user_id).exists()
