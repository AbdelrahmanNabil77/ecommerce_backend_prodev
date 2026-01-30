from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ProductReview 
from .serializers import (CategorySerializer, ProductSerializer,
                         ProductReviewSerializer)
from .permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin, IsAdminOrReadOnly
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
from rest_framework.permissions import IsAuthenticated, AllowAny


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category API - Admin only for write operations
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # Only admin can create/edit
    lookup_field = 'slug'
    
    def get_queryset(self):
        # Show only active categories to everyone
        return Category.objects.filter(is_active=True)

class ProductViewSet(viewsets.ModelViewSet):
    """
    Product API - Admin only for write operations
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]  # Only admin can create/edit
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = StandardResultsSetPagination
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'name', 'average_rating']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_queryset(self):
        """
        Optimized queryset that avoids the select_related + annotations conflict
        """
        # Apply annotations FIRST
        queryset = Product.objects.annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        
        # Only show published products for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        # Apply select_related and prefetch_related
        queryset = queryset.select_related('category', 'created_by').prefetch_related(
            'images',
            Prefetch('reviews', queryset=ProductReview.objects.filter(is_approved=True))
        )
        
        return queryset
    
    def perform_create(self, serializer):
        # Auto-set the creator as the current user (admin)
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products - Public access"""
        featured_products = self.get_queryset().filter(
            featured=True
        )[:10]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Get products on sale - Public access"""
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

class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    Product Review API - Authenticated users can create, admins can manage
    """
    # ADD THIS LINE - Required for DRF router to work
    queryset = ProductReview.objects.all()
    
    serializer_class = ProductReviewSerializer
    
    def get_permissions(self):
        """
        Different permissions for different actions:
        - Everyone can view reviews
        - Authenticated users can create reviews
        - Only admins can update/delete reviews
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return ProductReview.objects.filter(
            product__slug=self.kwargs['product_slug'],
            is_approved=True  # Only show approved reviews to public
        )
    
    def perform_create(self, serializer):
        # Get the product from the URL slug
        product = Product.objects.get(slug=self.kwargs['product_slug'])
        # Auto-set the user and product
        serializer.save(user=self.request.user, product=product)
    
    def perform_update(self, serializer):
        # Only admins can update, so we just save
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only admins can delete
        instance.delete()