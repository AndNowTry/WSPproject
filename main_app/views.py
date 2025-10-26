from datetime import datetime
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



class GetDataView(View):
    """
        Базовый пример ajax
    """
    def get(self, request):
        data = {                                  #тестил ajax
            "message": str(datetime.now())
        }
        return JsonResponse(data)



class ProductsPageListView(ListView):
    """
        Страничное представление продуктов
    """
    model = Products
    template_name = "main_app/products_page.html"
    context_object_name = 'products'

    def post(self, request, *args, **kwargs):
        self.category = request.POST.get('category')
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ProductsPageListView.model.objects.all()
        category = getattr(self, 'category', None)
        if category:
            queryset = queryset.filter(category=category)
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
        Страничка продукта
    """
