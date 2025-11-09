from datetime import datetime
from itertools import product
from urllib.parse import unquote

from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView
from django.http import JsonResponse
from main_app.models import Products, MainCategory, SecondaryCategory, TripleCategory



class HomePageView(TemplateView):
    """
        Главная страничка при начальной загрузке сайта
    """
    template_name = "main_app/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = 'maslo' #тестил
        context['Catalog'] = '' # тестил
        return context



class ProductsPageListView(ListView):
    """
        Страничное представление продуктов
    """
    model = Products
    template_name = "main_app/products_page.html"
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["category_name"] = self.kwargs.get('name')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('name')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset



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



class ProductPageView(TemplateView):
    """
        Страничное представление продукта
    """
    template_name = "main_app/product_cart_page.html"

    def get(self, request, *args, **kwargs):
        name = unquote(kwargs.get('name'))
        product = Products.objects.get(name = name)
        return render(request, self.template_name, {"name": product.name, "object": product})






