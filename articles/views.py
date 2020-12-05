from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from markdownx.utils import markdownify

from . import forms
from .forms import EditArticle
from .models import Article, Tag, Comment, LikeOfArticle, FavouriteArticles

NUMBER_OF_ARTICLES_PER_PAGE = 10


def articles_by_tag(request, tag):
    articles = Article.objects.filter(tag__title=tag, status='published')
    return render(request, 'articles/articles_by_tag.html', {'articles': articles, 'tag': tag})


def article_list(request):
    all_articles = Article.objects.filter(status='published').order_by('date')
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/article_list.html', {'articles': articles})


def article_detail(request, slug):
    form = forms.CommentForms(request.POST)
    article = Article.objects.get(slug=slug)
    comments_count = len(article.comment_set.all()) - len(
        Comment.objects.filter(parent__isnull=False, status='deleted'))
    liked = LikeOfArticle.objects.filter(article__id=article.id, user_id=request.user.id).exists()
    count_of_likes = article.count_of_likes

    favourite = FavouriteArticles.objects.filter(article__id=article.id, user_id=request.user.id).exists()

    body = markdownify(article.body)
    return render(request, 'articles/article_detail.html',
                  {'article': article, 'body': body, 'form': form, 'comments_count': comments_count, 'liked': liked,
                   'count_of_likes': count_of_likes, 'favourite': favourite})


def article_delete(request, slug):
    try:
        article = Article.objects.get(slug=slug)
        if request.user.username == article.author.username:
            Article.objects.filter(slug=slug).delete()
    except Article.DoesNotExist:
        pass
    return redirect('/')


@login_required(login_url="/accounts/login/")
def article_edit(request, slug):
    try:
        article = Article.objects.get(slug=slug)
        saved_tags = ', '.join(list(article.tag.values_list("title", flat=True)))
        if request.user.username == article.author.username:
            form = EditArticle(request.POST or None, instance=article)
            if form.is_valid():
                instance = form.save(commit=False)
                if form.data['tag']:
                    new_tags = form.data['tag'].split(',')
                    for i, j in enumerate(new_tags):
                        tag, created = Tag.objects.get_or_create(title=j.strip().lower())
                        new_tags[i] = tag
                    instance.tag.clear()
                    instance.tag.add(*new_tags)
                instance.save()
                return redirect('articles:detail', slug=slug)
        else:
            return redirect('/')
    except Article.DoesNotExist:
        return redirect('/')
    return render(request, 'articles/article_edit.html', {'form': form, 'article': article, 'tags': saved_tags})


@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            # save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            if form.data['tag']:
                tags = form.data['tag'].split(',')
                for i, j in enumerate(tags):
                    tag, created = Tag.objects.get_or_create(title=j.strip().lower())
                    tags[i] = tag
                instance.tag.add(*tags)
                instance.save()
            return redirect('articles:detail', slug=form.data['slug'])
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form': form})


def article_search(request):
    query = request.GET.get('q')
    all_articles = Article.objects.filter(
        Q(title__icontains=query) | Q(body__icontains=query) | Q(author__username__icontains=query)
    ).filter(status='published').order_by('date')
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'search.html', {'articles': articles, 'is_articles': True, 'query': query})


def article_tag_search(request):
    query = request.GET.get('q')
    all_tags = Tag.objects.filter(Q(title__icontains=query)).order_by('title')
    paginator = Paginator(all_tags, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    tags = paginator.get_page(page)
    return render(request, 'search.html', {'tags': tags, 'is_tags': True, 'query': query})


@login_required(login_url="/accounts/login/")
def add_comment(request, pk):
    form = forms.CommentForms(request.POST)
    article = Article.objects.get(id=pk)
    if form.is_valid():
        form = form.save(commit=False)
        if request.POST.get('parent', None):
            form.parent_id = int(request.POST.get('parent'))
        form.article = article
        form.author = request.user
        form.save()
    return redirect('articles:detail', article.slug)


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    slug = comment.article.slug
    comment.status = 'deleted'
    comment.save(update_fields=['status'])
    return redirect('articles:detail', slug)


@login_required(login_url="/accounts/login/")
def liking(request):
    if request.method == 'POST':
        article_id = request.POST['article_id']
        obj, liked = LikeOfArticle.objects.update_or_create(user_id=request.user.id, article_id=article_id)
        if not liked:
            obj.delete()
        likes = LikeOfArticle.objects.filter(article__id=article_id)
        count_of_likes = likes.count()
        return JsonResponse({'liked': liked, 'count_of_likes': count_of_likes}, status=201)
    else:
        return JsonResponse({'error': 'Error'}, status=400)


@login_required(login_url="/accounts/login/")
def add_to_favourite(request):
    if request.method == 'POST':
        article_id = request.POST['article_id']
        obj, favourite = FavouriteArticles.objects.get_or_create(user_id=request.user.id, article_id=article_id)
        if not favourite:
            obj.delete()
        return JsonResponse({'favourite': favourite}, status=201)
    else:
        return JsonResponse({'error': 'Error'}, status=400)


def favourite_articles(request):
    user_id = request.user.id
    favourite_ids = [i.article_id for i in FavouriteArticles.objects.filter(user_id=user_id).only('article_id')]
    all_articles = Article.objects.filter(id__in=favourite_ids)
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/favourite_articles.html', {'articles': articles})
