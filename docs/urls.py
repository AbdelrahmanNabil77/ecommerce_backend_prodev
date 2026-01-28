from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """API Overview"""
    endpoints = {
        'Authentication': {
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'refresh': '/api/auth/refresh/',
            'profile': '/api/auth/profile/',
        },
        'Products': {
            'list': '/api/products/',
            'detail': '/api/products/{slug}/',
            'search': '/api/products/?search={query}',
            'filter': '/api/products/?min_price=10&max_price=100',
        },
        'Categories': {
            'list': '/api/categories/',
            'detail': '/api/categories/{slug}/',
        }
    }
    return Response(endpoints)

urlpatterns = [
    path('', api_overview, name='api-overview'),
]