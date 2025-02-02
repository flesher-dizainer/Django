from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from .models import Post, Category, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, 'main.html')


def about(request):
    context = {
        "title": "О нас",
        "text": "Страница с информацией о нас",
    }
    return render(request, 'about.html', context)


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
            posts = Post.objects.none()
    else:
        posts = Post.objects.all()
    # Добавляем пагинацию
    paginator = Paginator(posts, 6)  # 6 постов на страницу
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
    }
    return render(request, 'python_blog/blog.html', context)


def catalog_categories(request):
    categories = Category.objects.annotate(posts_count=Count('post'))
    return render(request, 'python_blog/catalog_categories.html', {'categories': categories})


def catalog_tags(request):
    tags = Tag.objects.annotate(posts_count=Count('post'))
    return render(request, 'python_blog/catalog_tags.html', {'tags': tags})


def post_detail(request, slug):
    Post.objects.filter(slug=slug).update(views=F('views') + 1)
    post = get_object_or_404(Post.objects.select_related('category', 'author')
                             .prefetch_related('tags'), slug=slug)
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


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'python_blog/post_form.html', {'form': form})


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        initial_tags = ', '.join(tag.name for tag in post.tags.all())
        form = PostForm(instance=post, initial={'tags': initial_tags})
    return render(request, 'python_blog/post_form.html', {'form': form, 'post': post})
