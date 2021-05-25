from rest_framework import serializers

from buyer.models import ItemInOrder, Order
from .models import Shop, Category, Product, Parameter, ProductParameter


class RecursiveField(serializers.Serializer):
    '''сериализатор для рекурсивного вывода вложенных данных'''
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value']


class ProductSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField()
    product_info_parameters = ProductParameterSerializer(read_only=True, many=True)
    name = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'external_id', 'category', 'name', 'model', 'shop', 'quantity',
                  'price', 'price_rrc', 'product_info_parameters')


class ShopCreteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Shop
        fields = '__all__'


class ShopBaseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'user']


class ShopDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    # categories = RecursiveField(read_only=True, many=True)
    products_info = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'user', 'categories', 'products_info']


class ShopsListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'state', 'url', 'user']


class ShopOrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    contact = serializers.StringRelatedField()

    class Meta:
        model = Order
        exclude = ('is_active',)

