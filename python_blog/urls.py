"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from python_blog.views import *
app_name = 'blog'  # Добавляем неймспейс
urlpatterns = [
    path('', catalog_posts, name='catalog_posts'),
    path('categories/', catalog_categories, name='catalog_categories'),
    path('categories/<slug:category_slug>/', category_detail, name='category_detail'),
    path('tags/', catalog_tags, name='catalog_tags'),
    path('tags/<slug:tag_slug>/', tag_detail, name='tag_detail'),
    path('<slug:post_slug>/', post_detail, name='post_detail'),
]
