from .serializers import RegisterSerializer
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .serializers import ProductCreateSerializer, ProductImageUploadSerializer, OrderSerializer
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.generics import CreateAPIView, DestroyAPIView
from .models import Cart
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from rest_framework import status





class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)




class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'



class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]


class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageUploadSerializer
    permission_classes = [IsAuthenticated]


# Savatchani olish (faqat login qilingan foydalanuvchi uchun)
class CartDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

# Savatchaga mahsulot qo‘shish
class CartItemAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = Product.objects.get(id=product_id)

        # CartItem qo‘shish yoki yangilash
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

# Savatchadan mahsulotni o‘chirish
class CartItemDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Buyurtmaga mahsulotlarni qo‘shish
        order_items = []
        for item in cart.items.all():
            order_items.append({
                'product': item.product,
                'quantity': item.quantity,
            })

        # Cartni tozalash
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)

        # To‘lovni tasdiqlash
        order.is_paid = True
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)



class CartAddAPIView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CartDeleteAPIView(DestroyAPIView):
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)





