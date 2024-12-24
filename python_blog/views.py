from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from python_blog.blog_data import dataset
# from django.http import HttpResponse

CATEGORIES = [
    {'slug': 'python', 'name': 'Python'},
    {'slug': 'django', 'name': 'Django'},
    {'slug': 'postgresql', 'name': 'PostgreSQL'},
    {'slug': 'docker', 'name': 'Docker'},
    {'slug': 'linux', 'name': 'Linux'},
]
POSTS = [
    {'slug': 'blog', 'name': 'Blog'},
    {'slug': 'home', 'name': 'Home'},
    {'slug': 'about', 'name': 'About'},
    {'slug': 'contact', 'name': 'Contact'},
    {'slug': 'privacy', 'name': 'Privacy'},
]
TAGS = [
    {'slug': 'Div', 'name': 'Div'},

]


def main(request):

    return render(request, 'main.html' )


def about(request):
    context = {
        "title": "О нас",
        "text":"Страница с информацией о нас",
    }
    return render(request, 'about.html', context)


def catalog_posts(request):
    return render(request, 'python_blog/blog.html')


def catalog_categories(request):
    return render(request, 'python_blog/catalog_categories.html', {'categories': CATEGORIES})


def category_detail(request, category_slug):
    return render(request, 'python_blog/category_detail.html', {'category_slug': category_slug})


def catalog_tags(request):
    return render(request, 'python_blog/catalog_tags.html', {'tags': TAGS})


def tag_detail(request, tag_slug):
    return render(request, 'python_blog/tag_detail.html', {'tag_slug': tag_slug})


def post_detail(request, post_slug):
    return render(request, 'python_blog/post_detail.html', {'post_slug': post_slug})
