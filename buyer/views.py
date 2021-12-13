from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Contact
from accounts.serializers import ContactSerializer
from .models import Order, ItemInOrder
from .serializers import OrderSerializer, OrderItemSerializer, OrderItemAddSerializer

'''Вывод заказа/корзины пользователя'''
class OrderSerializerView(APIView):


    def get(self, request):
        user = request.user
        try:
            order = Order.objects.get(user=user, status='В корзине')
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'response': f'Уважаемый {request.user}, Ваша корзина пока пуста.',
                             'help_info': 'Перейдите по ссылке http://127.0.0.1:8000/api/v1/cart/create/'})

'''Добавление товара в заказ'''
class AddItemInOrderView(generics.CreateAPIView):

    serializer_class = OrderItemAddSerializer

    def get_queryset(self):
        order = Order.objects.get(user=self.request.user, status='В корзине')
        order.contact = Contact.objects.get(user=self.request.user)
        item = ItemInOrder.objects.filter(order=order)
        return item


'''Вывод заказанных товаров из заказа/корзины'''
class ItemsInOrderView(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = ItemInOrder.objects.all()

    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user, status='В корзине').first()
        items = ItemInOrder.objects.filter(order=order)
        return items


"""создать заказ"""
class OrderCreateView(APIView):

    def get(self, request):
        return Response({'info': "Необходимо зарегистрироваться как buyer"
                                 " и отправить пустой POST запрос по данному URL"})

    def post(self, request):
        user = request.user
        contact = Contact.objects.get(user=user)
        try:
            order = Order.objects.create(user=user, contact=contact, status='В корзине')
            order.save()
            return Response({'response': f'Корзина пользователя {user} создана'})
        except Exception as e:
            return Response({'response': e})


'''Подтверждение заказа в корзине / или вывод help_info'''
class CartConfirmView(APIView):
    def get(self, request):
        user = request.user
        try:
            order = Order.objects.get(user=user, status='В корзине')
            order.status = 'Подтвержден'
            order.is_active = True
            order.save()
            return Response({'response': 'Ваш заказ подтвержден.'})
        except ObjectDoesNotExist:
            return Response({'response': f'Уважаемый {request.user}, Ваша корзина пока пуста.',
                             'help_info': 'Перейдите по ссылке http://127.0.0.1:8000/api/v1/cart/create/'})


"""Отображние / Создание / Редактирование контакта пользователя Buyer"""
class ContactView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        contact = Contact.objects.filter(user=self.request.user)
        return contact
