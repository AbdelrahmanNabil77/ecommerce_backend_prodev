from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ProductReview 
from .serializers import (CategorySerializer, ProductSerializer,
                         ProductReviewSerializer)
from .permissions import IsOwnerOrReadOnly, IsProductOwnerOrAdmin
from .filters import ProductFilter
from .pagination import StandardResultsSetPagination
from django.db.models import Count, Avg, Q, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.db import models
from .models import Category, Product, ProductImage, ProductReview
from .serializers import CategorySerializer, ProductSerializer, ProductReviewSerializer
from .filters import ProductFilter
from .pagination import StandardResultsSetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

class ProductViewSet(viewsets.ModelViewSet):
    
  
    
    queryset = Product.objects.select_related('category', 'created_by')\
                             .prefetch_related('images', 'reviews')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['category', 'status', 'featured']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def upload_images(self, request, slug=None):
        product = self.get_object()
        # Handle multiple image uploads
        return Response(status=status.HTTP_201_CREATED)
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                      filters.OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = StandardResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.get_queryset().filter(
            featured=True, 
            status='published'
        )[:10]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        on_sale_products = self.get_queryset().filter(
            status='published',
            compare_price__gt=models.F('price')
        )
        page = self.paginate_queryset(on_sale_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(on_sale_products, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        """
        Optimized queryset that avoids the select_related + annotations conflict.
        """
        # Start with base queryset
        queryset = Product.objects.all()
        
        # Apply filters for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        # Apply annotations FIRST
        queryset = queryset.annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        
        # Then apply select_related and prefetch_related
        # Don't use select_related on created_by when we have annotations
        # Instead, we'll prefetch it
        queryset = queryset.select_related('category').prefetch_related(
            'images',
            Prefetch('reviews', queryset=ProductReview.objects.filter(is_approved=True))
        )
        
        return queryset
    
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return ProductReview.objects.filter(
            product__slug=self.kwargs['product_slug']
        )
    
    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs['product_slug'])
        serializer.save(user=self.request.user, product=product)
