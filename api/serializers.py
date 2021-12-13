
from rest_framework import serializers

from accounts.models import User #Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order, Contact





'''Класс контактов при заказе'''
# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
#         read_only_fields = ('id',)
#         extra_kwargs = {
#             'user': {'write_only': True}
#         }

'''класс пользователя "rest"'''
# class UserSerializer(serializers.ModelSerializer):
#     contacts = ContactSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'email', 'company', 'position', 'type', 'contacts')
#         read_only_fields = ('id',)
#
''' Список категорий '''
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name',)
#         read_only_fields = ('id',)
#
'''список магазинов'''
# class ShopsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = ('id', 'name', 'state',)
#         read_only_fields = ('id',)
#
'''Класс для магазина (проверка подлиности) и вывод информации'''
# class ShopDetailSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = Shop
#         fields = '__all__'
#         # read_only_fields = ('id',)
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.StringRelatedField()
#
#     class Meta:
#         model = Product
#         fields = ('name', 'category',)
#
'''Класс параметров продукта'''
# class ProductParameterSerializer(serializers.ModelSerializer):
#     parameter = serializers.StringRelatedField()
#
#     class Meta:
#         model = ProductParameter
#         fields = ('parameter', 'value',)
#
'''Класс информации продуктов'''
# class ProductInfoSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)
#     product_parameters = ProductParameterSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = ProductInfo
#         fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
#         read_only_fields = ('id',)
#
'''Класс формирования ордера/заказа'''
# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ('id', 'product_info', 'quantity', 'order',)
#         read_only_fields = ('id',)
#         extra_kwargs = {
#             'order': {'write_only': True}
#         }
#
'''Класс создания  заказа'''
# class OrderItemCreateSerializer(OrderItemSerializer):
#     product_info = ProductInfoSerializer(read_only=True)
#
'''Класс оформления заказа'''
# class OrderSerializer(serializers.ModelSerializer):
#     ordered_items = OrderItemCreateSerializer(read_only=True, many=True)
#
#     total_sum = serializers.IntegerField()
#     contact = ContactSerializer(read_only=True)
#
#     class Meta:
#         model = Order
#         fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact',)
#         read_only_fields = ('id',)
#
'''информация пользователя'''
# class UsersListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'type']
#
'''возможно автомотическое присваивание текущего юзера к созданной модели'''
# class UserDetailSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = User
#         fields = ['user', 'email', 'type', 'company', 'position', 'is_active']
