from django.contrib import admin
from django.urls import path, include
from articles import views as article_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('', article_views.article_list, name="home")
]
