from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductReview
from .serializers import (CategorySerializer, ProductSerializer,
                         ProductReviewSerializer)
from .permissions import IsOwnerOrReadOnly, IsProductOwnerOrAdmin

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                      filters.OrderingFilter]
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
