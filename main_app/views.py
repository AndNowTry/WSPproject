from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse



# Create your views here.
class HomePageView(TemplateView):
    template_name = "main_app/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['latest_articles'] = 'maslo' #тестил
        context['Catalog'] =  # тестил



        return context



class GetDataView(View):
    def get(self, request):
        data = {                                  #тестил ajax
            "message": str(datetime.now())
        }
        return JsonResponse(data)


