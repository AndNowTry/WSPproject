import json
from main_app.models import MainCategory, SecondaryCategory, TripleCategory, Products
from user_app.models import Favorites, Orders
from django.core.serializers import serialize



def catalog_processor(request):
    """
        Данные для каталога в базовом шаблоне
    """
    main_categories = MainCategory.objects.all()
    secondary_categories = SecondaryCategory.objects.all()
    triple_categories = TripleCategory.objects.all()

    return {
        "main_categories": main_categories,
        "secondary_categories": secondary_categories,
        "triple_categories": triple_categories,
    }



def search_input_processor(request):
    """
        Данные для поиска
    """
    products = [
        {
            "id": p.id,
            "name": p.name,
            "category__name": p.category.name,
            "url": p.get_absolute_url()
        }
        for p in Products.objects.select_related("category")
    ]

    products.extend([
        {
            "id": c.id,
            "name": c.name,
            "url": c.get_absolute_url()
        }
        for c in TripleCategory.objects.select_related("category")
    ])

    return {
        'products_json': products
    }



def user_products_context(request):
    """
        Для избранного и заказов пользователя
    """
    if request.user.is_authenticated:
        user_favorites = set(Favorites.objects.filter(user=request.user).values_list('product_id', flat=True))
        user_orders = set(Orders.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        user_favorites = set()
        user_orders = set()

    return {
        'user_favorites': user_favorites,
        'user_orders': user_orders
    }




