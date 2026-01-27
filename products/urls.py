from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductReviewViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(
    r'products/(?P<product_slug>[^/.]+)/reviews',
    ProductReviewViewSet,
    basename='product-review'
)

urlpatterns = [
    path('', include(router.urls)),
]