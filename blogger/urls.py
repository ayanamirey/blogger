from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from articles import views as article_views
from accounts import views as accounts_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    re_path('^tags/(?P<tag>[\\w-]+)', article_views.articles_by_tag, name='articles-by-tag'),
    path('', article_views.article_list, name="home"),
    re_path(r'^@(?P<username>.+)$', views.username_detail, name='profile-details'),
    path('profile/', include('profiles.urls')),
    re_path(r'^markdownx/', include('markdownx.urls')),
    path('search/tags/', article_views.article_tag_search, name='search-tag'),
    path('search/users/', accounts_views.users_search, name='search-users'),
    path('search/', article_views.article_search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
