from datetime import datetime
from urllib.parse import unquote

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, View, ListView
from django.http import JsonResponse
from django.utils.timezone import now

from main_app.filters import ProductsFilter
from main_app.models import Products, MainCategory, SecondaryCategory, TripleCategory, Promotions
from user_app.models import Favorites, Orders

@method_decorator(never_cache, name='dispatch')
class HomePageView(TemplateView):
    """
        Главная страничка при начальной загрузке сайта
    """
    template_name = "main_app/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promotions'] = Promotions.objects.filter(
            start_datetime__lte= now(),
            end_datetime__gte=now()
        )
        context["products"] = Products.objects.filter(is_active=True)
        return context


@method_decorator(never_cache, name='dispatch')
class ProductsPageListView(ListView):
    model = Products
    template_name = "main_app/products_page.html"
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        category_param = self.kwargs.get('name')

        if not category_param:
            return queryset

        if "_____search_____" in category_param:
            category_name, search_string = category_param.split("_____search_____")
            queryset = queryset.filter(
                category__name__iexact=category_name.strip(),
                name__icontains=search_string.strip()
            )
            category_name = category_name.strip()
        else:
            queryset = queryset.filter(
                category__name__iexact=category_param.strip()
            )
            category_name = category_param.strip()

        self.category = TripleCategory.objects.get(name__iexact=category_name)

        self.filterset = ProductsFilter(
            self.request.GET,
            queryset=queryset,
            category=self.category
        )

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_name"] = self.kwargs.get('name').replace(
            '_____search_____', ': '
        )
        context["filter"] = self.filterset
        return context



class CategoryPageView(TemplateView):
    """
        Страничное представление категорий
    """
    template_name = "main_app/categories_page.html"

    def get(self, request, *args, **kwargs):
        level = kwargs.get('level')
        name = kwargs.get('name')

        if level not in ['main', 'second', 'triple']:
            return None
        else:
            if level == "main":
                categories = MainCategory.objects.all()
                return render(request, self.template_name, {"level": "Главная категория", "objects": categories})
            if level == "second":
                categories = SecondaryCategory.objects.only("name", "photo").filter(category__name=name)
                return render(request, self.template_name, {"level": "Вторичная категория", "objects": categories})
            if level == "triple":
                categories = TripleCategory.objects.only("name", "photo").filter(category__name=name)
                return render(request, self.template_name, {"level": "Третичная категория", "objects": categories})


@method_decorator(never_cache, name='dispatch')
class ProductPageView(TemplateView):
    """
        Страничное представление продукта
    """
    template_name = "main_app/product_cart_page.html"

    def get(self, request, *args, **kwargs):
        name = unquote(kwargs.get('name'))
        product = Products.objects.get(name = name)
        return render(request, self.template_name, {"name": product.name, "object": product})



@method_decorator(never_cache, name='dispatch')
class FavoriteCartsPageView(LoginRequiredMixin, TemplateView):
    """
        Страничное представление избранных
    """
    template_name = "main_app/favorite_cards_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = (
            Favorites.objects
            .select_related('product')
            .filter(user=self.request.user)
        )
        return context



@method_decorator(never_cache, name='dispatch')
class OrderCartsPageView(LoginRequiredMixin, TemplateView):
    """
        Страничное представление заказов
     """
    template_name = "main_app/order_cards_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = (
            Orders.objects
            .select_related('product')
            .filter(user=self.request.user)
        )
        return context



@require_POST
def add_favorite(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    prod = get_object_or_404(Products, id=product_id)
    Favorites.objects.get_or_create(user=request.user, product=prod)
    return JsonResponse({'success': True, 'product_id': prod.id})



@require_POST
def remove_favorite(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    Favorites.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({'success': True, 'product_id': product_id})



@require_POST
def create_order(request, product_id):
    """
        Создает заказ пользователя
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    product = get_object_or_404(Products, id=product_id)
    Orders.objects.get_or_create(user=request.user, product=product, is_paid=False)
    return JsonResponse({'success': True, 'product_id': product.id})



@require_POST
def delete_order(request, product_id):
    """
        Удаляет заказ пользователя
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    Orders.objects.filter(user=request.user, product_id=product_id, is_paid=False).delete()
    return JsonResponse({'success': True, 'product_id': product_id})






