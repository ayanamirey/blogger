from django.shortcuts import render
from django.contrib.auth.models import User
from articles.models import Article


def homepage(request):
    return render(request, 'homepage.html')


def username_detail(request, username):
    try:
        username = User.objects.get(username=username)
    except User.DoesNotExist:
        username = None
    articles = Article.objects.filter(author=username)
    return render(request, 'profile/user_details.html', {'username': username, 'articles': articles})
