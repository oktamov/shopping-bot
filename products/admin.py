from django.contrib import admin
from .models import Category, Product, Order, Cart


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('id',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'created_at', 'count')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category__name')
    ordering = ('-created_at', 'name')


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone', 'address', 'created_at', 'is_viewed', 'is_accepted', 'is_sold')
    list_filter = ('is_viewed', 'is_accepted', 'is_sold', 'created_at')
    search_fields = ('name', 'phone', 'user__username')
    ordering = ('-created_at', 'name')
    list_editable = ('is_viewed', 'is_accepted', 'is_sold')


admin.site.register(Order, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'order', 'product', 'price', 'quantity', 'created_at', 'total_price', 'total_quantity')
    list_filter = ('user', 'order', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')
    ordering = ('-created_at',)


admin.site.register(Cart, CartAdmin)
