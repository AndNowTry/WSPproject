from django.urls import path, re_path
from .views import HomePageView, GetDataView, ProductsPageListView, CategoryPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('get-data/', GetDataView.as_view(), name="get_data"),
    path('category/<str:level>:<str:name>', CategoryPageView.as_view(), name='category'),
    path('products/', ProductsPageListView.as_view(), name="products")
]