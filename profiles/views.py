import os

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

import json

from articles.models import Article
from profiles.forms import UserForm, ProfileForm, AvatarForm, SocialNetworkForm
from profiles.models import Profile, SocialNetwork, ConnectToSocialAccount


@login_required
@transaction.atomic
def profile_detail(request):
    social_networks = SocialNetwork.objects.all()
    social_accounts = ConnectToSocialAccount.objects.filter(user_id=request.user.id)
    # social_accounts = json.loads(serializers.serialize('json', social_accounts))
    try:
        username = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user__username=username)
    except User.DoesNotExist:
        profile = None
        username = None
    except Profile.DoesNotExist:
        profile = None
    articles = Article.objects.filter(author=username, status='published')

    if request.method == 'POST':
        if '_profile_edit' in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, ('Your profile was successfully updated!'))
                return redirect('/profile', username=username)
            else:
                messages.error(request, ('Please correct the error below.'))
        elif '_change_password' in request.POST:
            password_change_form = PasswordChangeForm(request.user, request.POST)
            if password_change_form.is_valid():
                user = password_change_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, ('Your password was successfully changed!'))
                return redirect('/profile', username=username)
            else:
                messages.error(request, ('Please correct the error below.'))
        elif '_social_account' in request.POST:
            socials = [[x[3:], y] for x, y in request.POST.items() if x[0:3] == '_s_']
            for i in socials:
                social = SocialNetwork.objects.filter(title=i[0])
                if social and i[1] != '':
                    ConnectToSocialAccount.objects.update_or_create(user_id=request.user.id,
                                                                    social_network_id=social[0].id,
                                                                    defaults={
                                                                        'username': i[1],
                                                                    })

            return redirect('/profile', username=username)

        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_change_form = PasswordChangeForm(request.user)
        avatar_form = AvatarForm(request.profile.user)
        social_form = SocialNetworkForm()
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_change_form = PasswordChangeForm(request.user)
        avatar_form = AvatarForm(instance=request.user.profile)
        social_form = SocialNetworkForm()

    user = request.user
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'profile/profile_details.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_change_form': password_change_form,
        'avatar_form': avatar_form,
        'social_form': social_form,
        'avatar': username.profile.avatar,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'google_login': google_login,
        'can_disconnect': can_disconnect,
        'articles': articles,
        'profile': profile,
        'social_networks': social_networks,
        'social_accounts': social_accounts,
    })


@login_required
def update_profile(request):
    try:
        username = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user__username=username)
    except User.DoesNotExist:
        profile = None
    articles = Article.objects.filter(author=username, status='published')
    return render(request, 'profile/profile_details.html',
                  {'articles': articles, 'profile': profile})


NUMBER_OF_ARTICLES_PER_PAGE = 10


def draft_articles(request):
    username = request.user.username
    all_articles = Article.objects.filter(author__username=username)
    published = all_articles.filter(status='published')
    draft = all_articles.filter(status='draft')
    paginator = Paginator(draft, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'profile/my_articles.html',
                  {'username': request.user, 'articles': articles, 'published_count': len(published),
                   'draft_count': len(draft), 'draft': True})


def published_articles(request):
    username = request.user.username
    all_articles = Article.objects.filter(author__username=username)
    published = all_articles.filter(status='published')
    draft = all_articles.filter(status='draft')
    paginator = Paginator(published, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'profile/my_articles.html',
                  {'username': request.user, 'articles': articles, 'published_count': len(published),
                   'draft_count': len(draft), 'published': True})


def set_avatar(request):
    if request.method == "POST":
        old_image = ''
        if request.user.profile.avatar:
            old_image = request.user.profile.avatar.path
        avatar_form = AvatarForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if avatar_form.is_valid():
            if os.path.exists(old_image):
                os.remove(old_image)
            avatar_form.user_id = request.user.id
            avatar_form.save()
    return redirect('profiles:profile-details')


def delete_avatar(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.user.profile.avatar:
        avatar_path = request.user.profile.avatar.path
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
            profile.avatar = ''
            profile.save()
    return redirect('profiles:profile-details')
