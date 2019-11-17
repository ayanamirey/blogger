from django.contrib import admin
from django.urls import path, include, re_path
from articles import views as article_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('', article_views.article_list, name="home"),
    re_path(r'^@(?P<username>.+)$', views.username_detail)
]
