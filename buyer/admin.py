from django.contrib import admin

from .models import Order, ItemInOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created', 'updated',
                    'total_items_count', 'total_price']
    list_display_links = ['user']
    list_filter = ['user', 'status', 'created', 'updated', ]


@admin.register(ItemInOrder)
class ItemInOrdermAdmin(admin.ModelAdmin):
    list_display = ['order', 'category', 'shop', 'product_name', 'model',
                    'quantity', 'price_per_item', 'total_price']