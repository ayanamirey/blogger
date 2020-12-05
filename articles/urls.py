from django.urls import path, re_path
from . import views

app_name = 'articles'

urlpatterns = [
    path('liking', views.liking, name='liking'),
    path('add_to_favourite', views.add_to_favourite, name='liking'),
    path('favourite-articles', views.favourite_articles, name='favourite-articles'),
    path('', views.article_list, name="list"),
    path('new', views.article_create, name="create"),
    re_path('delete-comment/(?P<pk>\\d+)', views.delete_comment, name='delete-comment'),
    re_path('add-comment/(?P<pk>\\d+)', views.add_comment, name='add-comment'),
    re_path('(?P<slug>[\\w-]+)/edit', views.article_edit, name='edit'),
    re_path('(?P<slug>[\\w-]+)/delete', views.article_delete, name='delete'),
    re_path('(?P<slug>[\\w-]+)/$', views.article_detail, name='detail')
]

