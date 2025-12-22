from django.urls import path, re_path
from .views import HomePageView, ProductsPageListView, CategoryPageView, ProductPageView, create_order, remove_favorite, \
    add_favorite, delete_order, FavoriteCartsPageView, OrderCartsPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('category/<str:level>:<str:name>', CategoryPageView.as_view(), name='category'),
    path('products/category:<str:name>', ProductsPageListView.as_view(), name="products"),
    re_path(r'^product/(?P<name>.+)/$', ProductPageView.as_view(), name='product'),
    path('favorite/add/<int:product_id>/', add_favorite, name='add_favorite'),
    path('favorite/remove/<int:product_id>/', remove_favorite, name='remove_favorite'),
    path('order/create/<int:product_id>/', create_order, name='create_order'),
    path('order/delete/<int:product_id>/', delete_order, name='delete_order'),
    path('favorites', FavoriteCartsPageView.as_view(), name='favorites'),
    path('orders', OrderCartsPageView.as_view(), name='orders'),
]