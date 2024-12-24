MENU_ITEMS = [
    {"title": "Главная", "url_name": "main"},
    {"title": "Блог", "url_name": "blog:blog"},
    {"title": "Категории", "url_name": "blog:catalog_categories"},
    {"title": "Теги", "url_name": "blog:catalog_tags"},
    {"title": "About", "url_name": "about"},
]

def menu_items(request):
    return {
        'menu_items': MENU_ITEMS,
    }