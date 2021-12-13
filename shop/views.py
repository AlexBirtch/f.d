from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from django.core.mail import send_mail

from orders.celery import send_confirm_mail
from orders.settings import EMAIL_HOST_USER

from yaml import load as load_yaml

from api.permissions import IsShop
from buyer.models import ItemInOrder, Order
from shop.models import Shop, Category, Product, Parameter, ProductParameter, Brand
from shop.serializers import (ShopDetailSerializer, ShopCreteSerializer,
                              ShopsListSerializer, CategorySerializer, ProductSerializer, ShopBaseSerializer,
                              ShopOrderSerializer)
from rest_framework.permissions import IsAuthenticated


"""создание магазина"""
class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopCreteSerializer
    permission_classes = (IsAuthenticated, IsShop)


"""представление всех магазинов"""
class ShopsListView(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopsListSerializer
    # permission_classes = (IsAdminUser,)


"""детальное представление магазина"""
class ShopDetailView(viewsets.ModelViewSet):
    serializer_class = ShopDetailSerializer

    def get_queryset(self):
        shop = Shop.objects.filter(user=self.request.user)
        return shop



'''Базовое представление магазина с возможностью редактирования и удаления'''
class ShopBaseView(APIView):
    @staticmethod
    def get(request):
        try:
            shop = request.user.shop
            serializer = ShopBaseSerializer(shop)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'response': 'Shop does not exist'})

    @staticmethod
    def put(request):
        shop = request.user.shop
        serializer = ShopBaseSerializer(shop, request.data)

        data = {}
        if serializer.is_valid():
            serializer.save()
            data['request'] = f'Shop {shop} successfully updated'
        else:
            raise serializer.errors
        return Response(data)

    @staticmethod
    def delete(request):
        shop = request.user.shop
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''все категории'''
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


"""все товары"""
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination


"""получаем заказы магазина с возможностью изменения статуса заказа"""
class ShopOrdersView(viewsets.ModelViewSet):
    serializer_class = ShopOrderSerializer
    queryset = ItemInOrder.objects.all()

    def get_queryset(self):
        shop_owner = self.request.user
        shop = Shop.objects.get(user=shop_owner)
        order = Order.objects.filter(ordered_items__shop=shop).exclude(status='В корзине')

        '''отправка письма'''
        if self.request.method == 'PUT':
            # send_mail('Title', f'Заказ {order.first()}\nсменил статус на "{order.first().status}"',
            #           EMAIL_HOST_USER, ['birtch@afia.uno'], fail_silently=False)
            name = str(order.first().created)
            status = self.request.data['status']
            email = ['birtch@afia.uno']
            send_confirm_mail.delay({'name': name,
                                     'status': status,
                                     'email': email
                                     })
        return order



'''Импорт списка товаров из yaml'''
class ShopUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return Response({'status': False, 'error': 'Только для магазинов'}, status=status.HTTP_403_FORBIDDEN)

        yaml_file = request.data.get('yaml_file')

        if yaml_file:
            with open(yaml_file, 'rt', encoding='utf8') as f:
                data = load_yaml(f)
                pprint(data)

            shop, _ = Shop.objects.get_or_create(user_id=request.user.id, defaults={'name': data['shop']})
            for category in data['categories']:
                category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                category_object.shops.add(shop.id)
                category_object.save()

            pprint(Product.objects.filter(shop_id=shop.id))

            for item in data['goods']:
                category_ = Category.objects.get(pk=item['category'])
                item_brand_name, _ = Brand.objects.get_or_create(name=item['name'])
                product_ = Product.objects.create(
                    name=item_brand_name,
                    external_id=item['id'],
                    category=category_,
                    model=item['model'],
                    price=item['price'],
                    price_rrc=item['price_rrc'],
                    quantity=item['quantity'],
                    shop_id=shop.id)
                for name, value in item['parameters'].items():
                    parameter_id_, _ = Parameter.objects.get_or_create(name=name)
                    ProductParameter.objects.create(
                        product_info=Product.objects.get(pk=product_.pk),
                        parameter=Parameter.objects.get(pk=parameter_id_.pk),
                        value=value)

            if shop.name != data['shop']:
                return Response({'status': False, 'error': 'В файле указано некорректное название магазина!'},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': True})

        return Response({'status': False, 'error': 'Не указаны необходимые поля'},
                        status=status.HTTP_400_BAD_REQUEST)
