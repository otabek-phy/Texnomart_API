from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Cart
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Order)
def move_cart_items_to_order(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            instance.products.add(item.product)

        cart_items.delete()