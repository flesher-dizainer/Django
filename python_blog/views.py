from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.urls import reverse_lazy
from .models import Post, Category, Tag
from .forms import PostForm

def main(request):
    return render(request, 'main.html')


def about(request):
    context = {
        "title": "О нас",
        "text": "Страница с информацией о нас",
    }
    return render(request, 'about.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'python_blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            queries = Q()
            if self.request.GET.get('category') == 'on':
                queries |= Q(category__name__icontains=query)
            if self.request.GET.get('title') == 'on':
                queries |= Q(title__icontains=query)
            if self.request.GET.get('text') == 'on':
                queries |= Q(text__icontains=query)
            if self.request.GET.get('tags') == 'on':
                queries |= Q(tags__name__icontains=query)
            return Post.objects.filter(queries).distinct() if queries else Post.objects.none()
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'python_blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = super().get_object()
        Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(category=self.object.category).exclude(pk=self.object.pk)[:3]
        return context

    def get_queryset(self):
        return Post.objects.select_related('category', 'author').prefetch_related('tags')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'python_blog/post_form.html'
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'python_blog/post_form.html'
    success_url = reverse_lazy('blog:blog')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class CategoryListView(ListView):
    model = Category
    template_name = 'python_blog/catalog_categories.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'python_blog/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=self.object)
        return context

class TagListView(ListView):
    model = Tag
    template_name = 'python_blog/catalog_tags.html'
    context_object_name = 'tags'

class TagDetailView(DetailView):
    model = Tag
    template_name = 'python_blog/tag_detail.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(tags=self.object)
        return context
