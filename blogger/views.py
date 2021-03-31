from django.shortcuts import render
from django.contrib.auth.models import User
from articles.models import Article
from profiles.models import Profile, ConnectToSocialAccount


def homepage(request):
    return render(request, 'homepage.html')


def username_detail(request, username):
    try:
        username = User.objects.get(username=username)
        profile = Profile.objects.get(user__username=username)
    except User.DoesNotExist:
        username = None
        profile = None
    social_accounts = ConnectToSocialAccount.objects.filter(user_id=username.id)
    articles = Article.objects.filter(author=username)
    return render(request, 'profile/user_details.html',
                  {'articles': articles, 'profile': profile, 'social_accounts': social_accounts})
