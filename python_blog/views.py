from django.shortcuts import render, get_object_or_404
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
    posts = Post.objects.all()
    return render(request, 'python_blog/blog.html', {"posts": posts})


def catalog_categories(request):
    categories = Category.objects.all()
    return render(request, 'python_blog/catalog_categories.html', {'categories': categories})


def catalog_tags(request):
    tags = Tag.objects.all()
    return render(request, 'python_blog/catalog_tags.html', {'tags': tags})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'python_blog/category_detail.html', {'category': category})


def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    return render(request, 'python_blog/tag_detail.html', {'tag': tag})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'python_blog/post_detail.html', {'post': post})

