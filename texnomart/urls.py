from django.urls import path
from .views import RegisterView, CategoryListAPIView, ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView, ProductImageUploadView, CartDetailAPIView, CartItemAddAPIView, CartItemDeleteAPIView, OrderCreateAPIView, OrderPaymentAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    # API endpointlar
    path('categories/', CategoryListAPIView.as_view()),
    path('products/', ProductListAPIView.as_view()),
    path('products/<int:id>/', ProductDetailAPIView.as_view()),
    path('products/create/', ProductCreateAPIView.as_view()),
    path('products/upload-image/', ProductImageUploadView.as_view()),

    #######
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/add/', CartItemAddAPIView.as_view(), name='cart-item-add'),
    path('cart/delete/<int:item_id>/', CartItemDeleteAPIView.as_view(), name='cart-item-delete'),

    # buyurtma qilish
    path('order/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/payment/<int:order_id>/', OrderPaymentAPIView.as_view(), name='order-payment'),
]
