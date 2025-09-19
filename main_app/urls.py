from django.urls import path, re_path
from .views import HomePageView, GetDataView


urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('get-data/', GetDataView.as_view(), name="get_data")
]