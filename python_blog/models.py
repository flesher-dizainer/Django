from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='Слаг')
    description = models.TextField(blank=True, null=True, default='Без описания', verbose_name='Описание')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(str(self.name)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название тега')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='Слаг')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(str(self.name)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название поста')
    text = models.TextField(verbose_name='Текст поста')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Слаг')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(str(self.title)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
