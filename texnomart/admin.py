from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['title', 'category', 'price', 'created_at']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

