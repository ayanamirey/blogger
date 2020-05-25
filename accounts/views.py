from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('articles:list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('articles:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('articles:list')


NUMBER_OF_ARTICLES_PER_PAGE = 10


def users_search(request):
    query = request.GET.get('q')
    all_users = User.objects.filter(
        Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
    ).order_by('username')
    paginator = Paginator(all_users, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request, 'search.html', {'users': users, 'is_users': True, 'query': query})
