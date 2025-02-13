def menu_items(request):
    MENU_ITEMS = [
        {"title": "Главная", "url_name": "main"},
        {"title": "Блог", "url_name": "blog:blog"},
        {"title": "О нас", "url_name": "about"},
    ]
    for item in MENU_ITEMS:
        item['is_active'] = request.resolver_match.view_name == item['url_name']
    return {
        'menu_items': MENU_ITEMS,
    }