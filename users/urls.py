from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, AdminRegisterView, LoginView, UserProfileView

urlpatterns = [
    # Public endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Protected endpoints
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
]