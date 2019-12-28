from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect

from articles.models import Article
from profiles.forms import UserForm, ProfileForm
from profiles.models import Profile


@login_required
@transaction.atomic
def update_profile(request):
    try:
        username = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        username = None
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('/profile', username=username)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def profile_detail(request):
    try:
        username = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user__username=username)
    except User.DoesNotExist:
        profile = None
    articles = Article.objects.filter(author=username)
    return render(request, 'profile/profile_details.html',
                  {'articles': articles, 'profile': profile})
