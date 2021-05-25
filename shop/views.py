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


class ShopCreateView(generics.CreateAPIView):
    """создание магазина"""
    serializer_class = ShopCreteSerializer
    permission_classes = (IsAuthenticated, IsShop)


class ShopsListView(generics.ListAPIView):
    """представление всех магазинов"""
    queryset = Shop.objects.all()
    serializer_class = ShopsListSerializer
    # permission_classes = (IsAdminUser,)


class ShopDetailView(viewsets.ModelViewSet):
    """детальное представление магазина"""
    serializer_class = ShopDetailSerializer

    def get_queryset(self):
        shop = Shop.objects.filter(user=self.request.user)
        return shop


class ShopBaseView(APIView):
    """
    базовое представление магазина с возможностью редактирования и удаления
    """

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


# https://www.youtube.com/watch?v=C6S3dMt1s_M&t=5074s   at 1:24:55
# class ShopUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ShopDetailSerializer
#     queryset = Shop.objects.all()
#     permission_classes = (IsShopOwnerOrReadOnly,)
# тут у меня не заработало как надо....


class CategoryListView(generics.ListAPIView):
    """все категории"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductListView(generics.ListAPIView):
    """все товары"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination


class ShopOrdersView(viewsets.ModelViewSet):
    """получаем заказы магазина с возможностью изменения статуса заказа"""
    serializer_class = ShopOrderSerializer
    queryset = ItemInOrder.objects.all()

    def get_queryset(self):
        shop_owner = self.request.user
        shop = Shop.objects.get(user=shop_owner)
        order = Order.objects.filter(ordered_items__shop=shop).exclude(status='В корзине')

        # отправка письма
        if self.request.method == 'PUT':
            # send_mail('Title', f'Заказ {order.first()}\nсменил статус на "{order.first().status}"',
            #           EMAIL_HOST_USER, ['tihon49@gmail.com'], fail_silently=False)
            name = str(order.first().created)
            status = self.request.data['status']
            email = ['tihon49@gmail.com']
            send_confirm_mail.delay({'name': name,
                                     'status': status,
                                     'email': email
                                     })
        return order


class ShopUpdateView(APIView):
    """
    Импорт списка товаров из yaml
    """
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
