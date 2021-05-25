from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from shop.models import Category, Shop, Product, Brand
from accounts.models import User, Contact

STATE_CHOICES = (
    ('В корзине', 'В корзине'),
    ('Подтвержден', 'Подтвержден'),
    ('Отменен', 'Отменен'),
    ('Выполнен', 'Выполнен'),
)


class Order(models.Model):
    '''модел заказа'''
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='shopAPI', blank=True,
                             on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15, default='В корзине')
    contact = models.ForeignKey(Contact, verbose_name='Контакт', blank=True, null=True,
                                on_delete=models.CASCADE)
    total_price = models.DecimalField(verbose_name='Итоговая цена заказа', max_digits=10, decimal_places=2, default=0)
    total_items_count = models.IntegerField(verbose_name='Общее количество товаров в заказе', default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"
        ordering = ('-created',)

    def __str__(self):
        return f'{str(self.created)} : {self.user} : {self.status} {self.is_active}'


class ItemInOrder(models.Model):
    '''модель товара в заказе'''
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория товара', blank=True, null=True,
                                 on_delete=models.SET_NULL)
    shop = models.ForeignKey(Shop, verbose_name='магазин', blank=True, null=True, on_delete=models.SET_NULL)
    product_name = models.ForeignKey(Brand, verbose_name='Торговая марка', related_name='itemsInOrder',
                                     on_delete=models.CASCADE, blank=True)
    model = models.CharField('Модель', max_length=80)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД', blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price_per_item = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Общая стоимость')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = "Товары в заказе"
        # constraints = [
        #     models.UniqueConstraint(fields=['order_id', 'product_name'], name='unique_order_item'),
        # ]

    def __str__(self):
        return str(self.product_name)

    def save(self, *args, **kwargs):
        product = Product.objects.get(name=self.product_name, shop=self.shop, model=self.model)

        price_per_item = product.price
        self.price_per_item = price_per_item
        self.total_price = price_per_item * self.quantity

        super(ItemInOrder, self).save(*args, **kwargs)


# 1) source: https://www.youtube.com/watch?v=3wFpyKcVT_w&list=PLSWnD6rL-m9adebgpvvOLH5ASGJiznWdg&index=7  17:25
# 2) source: https://www.youtube.com/watch?v=Kc1Q_ayAeQk
@receiver(post_save, sender=ItemInOrder)
def item_in_order_post_save(sender, instance, created, **kwargs):
    '''функция перезаписи данных в модели товара в заказе'''
    all_items_in_order = ItemInOrder.objects.filter(order=instance.order)
    order_total_price = 0
    total_items_count_in_order = 0

    for item in all_items_in_order:
        #обновляем кол-во и общую стоимость товаров
        order_total_price += item.total_price
        total_items_count_in_order += item.quantity

    instance.order.total_price = order_total_price
    instance.order.total_items_count = total_items_count_in_order
    instance.order.save(force_update=True)
# post_save.connect(item_in_order_post_save, sender=ItemInOrder)


@receiver(post_delete, sender=ItemInOrder)
def item_in_order_post_delete(sender, instance, created=False, **kwargs):
    '''функция обновления цены и кол-ва товара в заказе при удалении из него какой-то позиции'''
    all_items_in_order = ItemInOrder.objects.filter(order=instance.order)
    order_total_price = 0
    total_items_count_in_order = 0

    for item in all_items_in_order:
        # обновляем кол-во и общую стоимость товаров
        order_total_price += item.total_price
        total_items_count_in_order += item.quantity

    instance.order.total_price = order_total_price
    instance.order.total_items_count = total_items_count_in_order
    instance.order.save(force_update=True)


