from django.urls import path
from .views import RegisterView, CategoryListAPIView, ProductListAPIView, ProductDetailAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    # API endpointlar
    path('categories/', CategoryListAPIView.as_view()),
    path('products/', ProductListAPIView.as_view()),
    path('products/<int:id>/', ProductDetailAPIView.as_view()),
]
