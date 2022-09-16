import sys
from datetime import datetime, timedelta
import hashlib
from django.db.models import Count, When, Case, IntegerField
from django.conf.global_settings import LANGUAGE_CODE
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.signing import Signer
from django.core import signing
from django.db import connection, connections
from markdownx.utils import markdownify

from accounts.models import FollowToCategory, FollowToUsers
from . import forms, r_db
from .forms import EditArticle
from .models import Article, Tag, Comment, LikeOfArticle, FavouriteArticles, ReportToArticle, ReportToComment, Category
from django.utils.translation import gettext as _

NUMBER_OF_ARTICLES_PER_PAGE = 10
signer = Signer()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def article_list(request):
    all_articles = Article.objects.filter(status='published').order_by('date')
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    print(sys.version)
    return render(request, 'articles/article_list.html', {'articles': articles, 'by_date': True})


def list_by_following(request):
    follow_categories = [x for x in
                         FollowToCategory.objects.filter(user_id=request.user.id).values_list('target_id', flat=True)]
    follow_users = [x for x in
                    FollowToUsers.objects.filter(user_id=request.user.id).values_list('target_id', flat=True)]
    all_articles = Article.objects.filter(Q(category_id__in=follow_categories) | Q(category_id__in=follow_users),
                                          status='published').order_by('date')
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/article_list.html', {'articles': articles, 'by_following': True})


def list_by_top(request):
    now = datetime.now()
    week_ago = now - timedelta(days=31)
    all_articles = Article.objects.filter(status='published', created_at__range=[week_ago, now]) \
        .annotate(by_formule=(Q())) \
        .order_by('by_formule')
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/article_list.html', {'articles': articles, 'by_top': True})


def list_most_liked(request):
    if request.method == 'POST':
        form = forms.NewTestForm(request.POST)
        text = ''
    else:
        form = forms.NewTestForm()
        form.data['to_date'] = datetime.now()
        form.data['from_date'] = datetime.now() - timedelta(days=1)
        text = '*По дефолту будет выбран промежуток в день'

    articles = Article.objects.filter(status='published').annotate(count_likes=Count(Case(
        When(likeofarticle__timestamp__range=[form.data['from_date'], form.data['to_date']], then=1),
        output_field=IntegerField(),
    ))).order_by('-count_likes')

    return render(request, 'articles/article_list.html',
                  {'context': articles, 'form': form, 'text': text, 'by_most_likes': True})


def list_most_comments(request):
    if request.method == 'POST':
        form = forms.NewTestForm(request.POST)
        text = ''
    else:
        form = forms.NewTestForm()
        form.data['to_date'] = datetime.now()
        form.data['from_date'] = datetime.now() - timedelta(days=1)
        text = '*По дефолту будет выбран промежуток в день'

    articles = Article.objects.filter(status='published').annotate(count_comments=Count(Case(
        When(comment__created_on__range=[form.data['from_date'], form.data['to_date']], then=True),
        output_field=IntegerField(),
    ))).order_by('-count_comments')

    return render(request, 'articles/article_list.html',
                  {'context': articles, 'form': form, 'text': text, 'by_most_comments': True})


'''
    1.5 * views + 3.5 * likes 
    Count("views") * 1.5 + 3.5 * Count('') 
'''


def articles_by_category(request, slug):
    category = Category.objects.get(slug=slug)
    all_articles = Article.objects.filter(category_id=category.id, status='published')
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/articles_by_category.html', {'category': category, 'articles': articles})


def articles_by_tag(request, tag):
    all_articles = Article.objects.filter(tag__title=tag, status='published')
    paginator = Paginator(all_articles, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/articles_by_tag.html', {'articles': articles, 'tag': tag})


def article_detail(request, slug):
    form_login = AuthenticationForm()
    form_signup = UserCreationForm()

    article_reports = ReportToArticle.TypeOfReport.choices
    comment_reports = ReportToComment.TypeOfReport.choices

    form_comment = forms.CommentForms(request.POST)
    article = Article.objects.get(slug=slug)
    comments_count = len(article.comment_set.all()) - len(Comment.objects.filter(article_id=article, status='deleted'))
    liked = LikeOfArticle.objects.filter(article__id=article.id, user_id=request.user.id).exists()
    count_of_likes = article.count_of_likes

    favourite = FavouriteArticles.objects.filter(article__id=article.id, user_id=request.user.id).exists()

    ip = get_client_ip(request)
    user_agent = request.META['HTTP_USER_AGENT']
    hash_data = hashlib.md5(bytes(ip + user_agent, 'utf-8'))

    if not r_db.exists(hash_data.hexdigest()):
        time = datetime.timestamp(datetime.now())
        token_ex = signing.dumps(time)
        r_db.set(token_ex, hash_data.hexdigest(), ex=120)
    else:
        token_ex = False

    body = markdownify(article.body)
    return render(request, 'articles/article_detail.html',
                  {'article': article, 'body': body, 'form_comment': form_comment, 'comments_count': comments_count,
                   'liked': liked, 'count_of_likes': count_of_likes, 'favourite': favourite, 'form_login': form_login,
                   'form_signup': form_signup, 'article_reports': article_reports, 'comment_reports': comment_reports,
                   'token_ex': token_ex})


def category_list(request):
    all_categories = Category.get_active_categories()
    paginator = Paginator(all_categories, NUMBER_OF_ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    categories = paginator.get_page(page)

    return render(request, 'articles/category_list.html', {'categories': categories})


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
        print(obj)
        print(liked)
        if not liked:
            obj.delete()
        likes = LikeOfArticle.objects.filter(article__id=article_id)
        count_of_likes = likes.count()
        return JsonResponse({'liked': liked, 'count_of_likes': count_of_likes},
                            status=201)
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


@login_required(login_url='/accounts/login/')
def report_to_comment(request):
    try:
        comment = Comment.objects.get(id=request.POST['comment_id'])
        if request.method == "POST":
            if 'report_comm' in request.POST and request.POST['report_comm'] != '' or 'report_type' in request.POST and \
                    request.POST['report_type'] != '':
                ReportToComment.objects.create(
                    comment_id=comment.id,
                    from_user_id=request.user.id,
                    type_of_report=request.POST['report_type'] if 'report_type' in request.POST else None,
                    extra_comment=request.POST['report_comm'] if 'report_comm' in request.POST else None
                )
            return JsonResponse({}, status=200)
    except:
        pass
    return JsonResponse({}, status=300)


@login_required(login_url='/accounts/login/')
def report_to_article(request):
    try:
        article = Comment.objects.get(id=request.POST['article_id'])
        if request.method == "POST":
            if 'report_comm' in request.POST and request.POST['report_comm'] != '' or 'report_type' in request.POST and \
                    request.POST['report_type'] != '':
                ReportToArticle.objects.create(
                    article_id=article.id,
                    from_user_id=request.user.id,
                    type_of_report=request.POST['report_type'] if 'report_type' in request.POST else None,
                    extra_comment=request.POST['report_comm'] if 'report_comm' in request.POST else None
                )
            return JsonResponse({}, status=200)
    except:
        pass
    return JsonResponse({}, status=300)


@login_required(login_url='/accounts/login/')
def following_to_category(request):
    try:
        if request.method == "POST":
            category = Category.objects.get(id=request.POST['category_id'])
            if request.POST['what'] == 'follow':
                follow, created = FollowToCategory.objects.get_or_create(target_id=category.id, user_id=request.user.id)
            if request.POST['what'] == 'unfollow':
                FollowToCategory.objects.filter(target_id=category.id, user_id=request.user.id).delete()
            return redirect('articles:category-list')
    except:
        pass
    return redirect('articles:category-list')


@login_required(login_url='/accounts/login/')
def following_to_user(request):
    target = User.objects.get(id=request.POST['user_id'])
    try:
        if request.method == "POST":
            if request.POST['what'] == 'follow':
                if target.id != request.user.id:
                    follow, created = FollowToUsers.objects.get_or_create(target_id=target.id, user_id=request.user.id)
                else:
                    pass
            if request.POST['what'] == 'unfollow':
                if target.id != request.user.id:
                    FollowToUsers.objects.filter(target_id=target.id, user_id=request.user.id).delete()
                else:
                    pass
            return redirect('users-profile', target.username)
    except:
        pass
    return redirect('users-profile', target.username)


def add_to_view(request):
    try:
        if 'token_ex' in request.GET and 'article_id' in request.GET:
            ip = get_client_ip(request)
            user_agent = request.META['HTTP_USER_AGENT']
            hash_data = hashlib.md5(bytes(ip + user_agent, 'utf-8')).hexdigest()
            token_ex = r_db.get(request.GET['token_ex'])
            my_time = signing.loads(request.GET['token_ex'])
            r_db.delete(request.GET['token_ex'])
            if (datetime.now().timestamp() - my_time) > 45 and not r_db.exists(hash_data):
                r_db.set(hash_data, 1, ex=172800)
                article = Article.objects.get(id=request.GET['article_id'])
                article.views = article.views + 1
                article.save()

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    except:
        return HttpResponse(status=400)
