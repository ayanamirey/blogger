from django.contrib import admin

from accounts.models import FollowToUsers, FollowToCategory


@admin.register(FollowToUsers)
class FollowToUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'following_date')


@admin.register(FollowToCategory)
class FollowToCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'following_date')
