from django.shortcuts import render
from django.contrib.auth.models import User
from articles.models import Article
from profiles.models import Profile


def homepage(request):
    return render(request, 'homepage.html')


def username_detail(request, username):
    try:
        username = User.objects.get(username=username)
        profile = Profile.objects.get(user__username=username)
    except User.DoesNotExist:
        username = None
        profile = None
    articles = Article.objects.filter(author=username)
    return render(request, 'profile/profile_details.html',
                  {'articles': articles, 'profile': profile})
