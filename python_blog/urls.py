from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, CategoryListView, CategoryDetailView,
    TagListView, TagDetailView
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blog'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('categories/', CategoryListView.as_view(), name='catalog_categories'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('tags/', TagListView.as_view(), name='catalog_tags'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag_detail'),
]
