from django.shortcuts import render

# Create your views here.
def index(request):
    data_for_temple = {}
    return render(request, 'main_app/home_page.html', data_for_temple)
