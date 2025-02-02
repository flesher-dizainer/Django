from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    # Поле для ввода тегов через запятую
    tags = forms.CharField(required=False, help_text='Введите теги через запятую')

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'tags']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_tags(self):
        # Очистка и валидация поля тегов
        tags_string = self.cleaned_data.get('tags', '')
        if tags_string:
            # Разбиваем строку по запятым и удаляем пробелы
            tag_names = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
            return tag_names
        return []

    def save(self, commit=True):
        # Сохраняем пост без коммита в базу
        post = super().save(commit=False)

        if commit:
            # Сохраняем пост
            post.save()

            # Обработка тегов
            post.tags.clear()  # Очищаем существующие теги
            tag_names = self.cleaned_data.get('tags', [])
            # Создаем или получаем теги и добавляем их к посту
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

        return post
