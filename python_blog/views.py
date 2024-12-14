from django.shortcuts import render
#from django.http import HttpResponse

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
TAGS=[
    {'slug': 'Div', 'name': 'Div'},

]
def main(request):
    return render(request, 'python_blog/main.html')

def catalog_posts(request):
    posts = POSTS
    return render(request, 'python_blog/catalog_posts.html', {'posts': posts})

def catalog_categories(request):
    categories = CATEGORIES  # Список категорий
    return render(request, 'python_blog/catalog_categories.html', {'categories': categories})

def category_detail(request, category_slug):
    return render(request, 'python_blog/category_detail.html', {'category_slug': category_slug})

def catalog_tags(request):
    return render(request, 'python_blog/catalog_tags.html',{'tags': TAGS})

def tag_detail(request, tag_slug):
    return render(request, 'python_blog/tag_detail.html', {'tag_slug': tag_slug})

def post_detail(request, post_slug):
    return render(request, 'python_blog/post_detail.html', {'post_slug': post_slug})
