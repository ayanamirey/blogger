from django.urls import path, re_path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_detail, name='profile-details'),
    # path('edit', views.update_profile, name='profile-update'),
    path('articles/draft', views.draft_articles, name='draft-articles'),
    path('articles/published', views.published_articles, name='published-articles'),
    path('set-avatar/', views.set_avatar, name='set-avatar')
]
