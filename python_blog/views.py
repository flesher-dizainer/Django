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


def catalog_posts(request):
    # post_list = Post.objects.select_related('category', 'author').prefetch_related('tags')
    # paginator = Paginator(post_list, 10)
    # page = request.GET.get('page')
    # posts = paginator.get_page(page)
    # return render(request, 'python_blog/blog.html', {'posts': posts})
    category = request.GET.get('category')
    query = request.GET.get('query')
    if query:
        if category:
            posts = Post.objects.filter(
                Q(category__name__icontains=category) |
                Q(title__icontains=query) |
                Q(text__icontains=query) |
                Q(tags__name__icontains=query),
            ).distinct()
        else:
            posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(text__icontains=query) |
                Q(tags__name__icontains=query),
            ).distinct()
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


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related('category', 'author')
                             .prefetch_related('tags'), slug=slug)
    Post.objects.filter(slug=slug).update(views=F('views') + 1)
    return render(request, 'python_blog/post_detail.html', {'post': post})
