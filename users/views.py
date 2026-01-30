from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, AdminRegisterSerializer

class RegisterView(generics.CreateAPIView):
    """
    Regular user registration - anyone can register
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create tokens for the user
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
class AdminRegisterView(generics.CreateAPIView):
    """
    Admin user registration - only existing admins can create new admins
    """
    serializer_class = AdminRegisterSerializer
    permission_classes = [permissions.IsAdminUser]

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile - user can view/update their own profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
