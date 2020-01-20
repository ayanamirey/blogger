from django.urls import path, re_path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name="list"),
    path('new', views.article_create, name="create"),
    re_path('(?P<slug>[\\w-]+)/edit', views.article_edit, name='article-edit'),
    re_path('(?P<slug>[\\w-]+)/delete', views.article_delete, name='article-delete'),
    re_path('(?P<slug>[\\w-]+)/$', views.article_detail, name='detail')
]
