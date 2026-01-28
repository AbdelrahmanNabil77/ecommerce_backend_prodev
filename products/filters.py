import django_filters
from django.db.models import Q
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price',
                                          lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price',
                                          lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__slug')
    search = django_filters.CharFilter(method='filter_search')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    
    class Meta:
        model = Product
        fields = ['category', 'featured', 'status']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(sku__icontains=value)
        )
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(quantity__gt=0)
        return queryset.filter(quantity=0)

class CategoryFilter(django_filters.FilterSet):
    parent = django_filters.CharFilter(field_name='parent__slug',
                                     lookup_expr='exact')
    has_products = django_filters.BooleanFilter(method='filter_has_products')
    
    def filter_has_products(self, queryset, name, value):
        if value:
            return queryset.filter(products__isnull=False).distinct()
        return queryset.filter(products__isnull=True)