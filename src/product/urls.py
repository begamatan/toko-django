from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view(), name='latest_products'),
    path('list/', views.ProductList.as_view(), name='product_list'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('<slug:category_slug>/', views.CategoryDetail.as_view(), name='category_detail'),
]