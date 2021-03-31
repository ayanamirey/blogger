from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Profile, SocialNetwork, ConnectToSocialAccount

# admin.site.register(LikeOfArticle)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


@admin.register(ConnectToSocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
