from django.urls import path, re_path
from .views import HomePageView, ProductsPageListView, CategoryPageView, ProductPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('category/<str:level>:<str:name>', CategoryPageView.as_view(), name='category'),
    path('products/category:<str:name>', ProductsPageListView.as_view(), name="products"),
    re_path(r'^product/(?P<name>.+)/$', ProductPageView.as_view(), name='product'),
]