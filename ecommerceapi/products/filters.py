from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    """Custom filter for Product model with range filtering"""
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_stock = filters.NumberFilter(field_name="stock", lookup_expr='gte')
    
    class Meta:
        model = Product
        fields = ['category', 'is_active']
