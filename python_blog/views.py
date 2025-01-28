from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from .models import Post, Category, Tag


def main(request):
    return render(request, 'main.html')


def about(request):
    context = {
        "title": "О нас",
        "text": "Страница с информацией о нас",
    }
    return render(request, 'about.html', context)


from django.db.models import Q

from django.db.models import Q


def catalog_posts(request):
    query = request.GET.get('query')
    category_check = request.GET.get('category') == 'on'
    title_check = request.GET.get('title') == 'on'
    text_check = request.GET.get('text') == 'on'
    tags_check = request.GET.get('tags') == 'on'

    if query:
        queries = Q()
        if category_check:
            queries |= Q(category__name__icontains=query)
        if title_check:
            queries |= Q(title__icontains=query)
        if text_check:
            queries |= Q(text__icontains=query)
        if tags_check:
            queries |= Q(tags__name__icontains=query)

        if queries:
            posts = Post.objects.filter(queries).distinct()
        else:
            posts = Post.objects.all()
    else:
        posts = Post.objects.all()

    categories = Category.objects.all()
    return render(request, 'python_blog/blog.html', {
        'posts': posts,
        'categories': categories,
    })


def catalog_categories(request):
    categories = Category.objects.annotate(posts_count=Count('post'))
    return render(request, 'python_blog/catalog_categories.html', {'categories': categories})


def catalog_tags(request):
    tags = Tag.objects.annotate(posts_count=Count('post'))
    return render(request, 'python_blog/catalog_tags.html', {'tags': tags})


def post_detail(request, slug):
    # увеличиваем количество просмотров
    Post.objects.filter(slug=slug).update(views=F('views') + 1)
    # получаем пост
    post = get_object_or_404(Post.objects.select_related('category', 'author')
                             .prefetch_related('tags'), slug=slug)
    # показываем пост
    return render(request, 'python_blog/post_detail.html', {'post': post})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    post_list = Post.objects.filter(category=category).select_related('author')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'python_blog/category_detail.html',
                  {'category': category, 'posts': posts})


def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    post_list = Post.objects.filter(tags=tag).select_related('author')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'python_blog/tag_detail.html',
                  {'tag': tag, 'posts': posts})
