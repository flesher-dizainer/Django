from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', catalog_posts, name='blog'),
    path('categories/', catalog_categories, name='catalog_categories'),
    path('categories/<slug:category_slug>/', category_detail, name='category_detail'),
    path('tags/', catalog_tags, name='catalog_tags'),
    path('tags/<slug:tag_slug>/', tag_detail, name='tag_detail'),
    path('<slug:slug>/', post_detail, name='post_detail'),
]
