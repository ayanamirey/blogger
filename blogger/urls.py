from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from articles import views as article_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    re_path('tags/(?P<tag>[\\w-]+)', article_views.articles_by_tag, name='articles-by-tag'),
    path('', article_views.article_list, name="home"),
    re_path(r'^@(?P<username>.+)$', views.username_detail),
    path('profile/', include('profiles.urls')),
    re_path(r'^markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
