from rest_framework import serializers
from accounts.serializers import ContactSerializer
from .models import Order, ItemInOrder


'''Класс формирования ордера/заказа'''
class OrderItemSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    product_name = serializers.StringRelatedField()

    class Meta:
        model = ItemInOrder
        fields = ['id', 'external_id', 'category', 'shop', 'product_name', 'model', 'quantity',
                  'price_per_item', 'total_price']
        read_only_fields = ['id', 'price_per_item', 'total_price']


'''Класс формирования/добавления ордера/заказа'''
class OrderItemAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInOrder
        fields = ['external_id', 'category', 'shop', 'product_name', 'model', 'quantity', 'order']


'''Создание ордера заказа'''
class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    contact = ContactSerializer

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['status', 'contact', 'total_price', 'total_items_count']


'''обновление информации о заказе'''
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'contact']
        read_only_fields = ['id']


'''описание ордера'''
class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemSerializer(read_only=True, many=True)
    total_price = serializers.IntegerField()
    total_items_count = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'status', 'total_items_count',
                  'total_price', 'contact', 'ordered_items')
        read_only_fields = ('id',)
