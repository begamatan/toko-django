from rest_framework import filters, generics

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Category, Product
from .serializers import CategorySerializer,ProductSerializer
# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL')

class LatestProductsList(generics.ListAPIView):
    queryset = Product.objects.all()[0:4]
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            'category__slug': self.kwargs['category_slug'],
            'slug': self.kwargs['product_slug'],
        }

        obj = get_object_or_404(queryset, **filter)
        return obj

class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            'slug': self.kwargs['category_slug']
        }

        obj = get_object_or_404(queryset, **filter)
        return obj

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super(CategoryDetail, self).dispatch(*args, **kwargs)
    
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']    