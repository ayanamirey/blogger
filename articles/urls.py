from django.urls import path, re_path
from . import views

app_name = 'articles'

urlpatterns = [
    path('liking', views.liking, name='liking'),
    path('add_to_view', views.add_to_view, name='add-to-view'),
    path('add_to_favourite', views.add_to_favourite, name='liking'),
    path('favourite-articles', views.favourite_articles, name='favourite-articles'),
    path('report-to-comment', views.report_to_comment, name='report-to-comment'),
    path('report-to-article', views.report_to_article, name='report-to-article'),
    path('follow-to-categories', views.following_to_category, name='follow-to-categories'),
    path('follow-to-users', views.following_to_user, name='follow-to-users'),
    path('', views.article_list, name="list"),
    path('following/', views.list_by_following, name="list-by-following"),
    path('top/', views.list_by_top, name="list-by-top"),
    path('categories/', views.category_list, name="category-list"),
    path('category/<str:slug>', views.articles_by_category, name="articles-by-category"),
    path('new', views.article_create, name="create"),
    re_path('delete-comment/(?P<pk>\\d+)', views.delete_comment, name='delete-comment'),
    re_path('add-comment/(?P<pk>\\d+)', views.add_comment, name='add-comment'),
    re_path('(?P<slug>[\\w-]+)/edit', views.article_edit, name='edit'),
    re_path('(?P<slug>[\\w-]+)/delete', views.article_delete, name='delete'),
    re_path('(?P<slug>[\\w-]+)/$', views.article_detail, name='detail')
]

