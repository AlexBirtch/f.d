from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator

from accounts.models import User

# STATE_CHOICES = (
#     ('basket', 'Статус корзины'),
#     ('new', 'Новый'),
#     ('confirmed', 'Подтвержден'),
#     ('assembled', 'Собран'),
#     ('sent', 'Отправлен'),
#     ('delivered', 'Доставлен'),
#     ('canceled', 'Отменен'),
# )



#
#
# class Contact(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь',
#                              related_name='contacts', blank=True,
#                              on_delete=models.CASCADE)
#
#     city = models.CharField(max_length=50, verbose_name='Город')
#     street = models.CharField(max_length=100, verbose_name='Улица')
#     house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
#     structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
#     building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
#     apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
#     phone = models.CharField(max_length=20, verbose_name='Телефон')
#
#     class Meta:
#         verbose_name = 'Контакты пользователя'
#         verbose_name_plural = "Список контактов пользователя"
#
#     def __str__(self):
#         return f'{self.city} {self.street} {self.house}'
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь',
#                              related_name='orders', blank=True,
#                              on_delete=models.CASCADE)
#     dt = models.DateTimeField(auto_now_add=True)
#     state = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)
#     contact = models.ForeignKey(Contact, verbose_name='Контакт',
#                                 blank=True, null=True,
#                                 on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = "Список заказ"
#         ordering = ('-dt',)
#
#     def __str__(self):
#         return str(self.dt)
#
#     # @property
#     # def sum(self):
#     #     return self.ordered_items.aggregate(total=Sum("quantity"))["total"]
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
#                               on_delete=models.CASCADE)
#
#     product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', related_name='ordered_items',
#                                      blank=True,
#                                      on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(verbose_name='Количество')
#
#     class Meta:
#         verbose_name = 'Заказанная позиция'
#         verbose_name_plural = "Список заказанных позиций"
#         constraints = [
#             models.UniqueConstraint(fields=['order_id', 'product_info'], name='unique_order_item'),
#         ]
#
#
# class ConfirmEmailToken(models.Model):
#     class Meta:
#         verbose_name = 'Токен подтверждения Email'
#         verbose_name_plural = 'Токены подтверждения Email'
#
#     @staticmethod
#     def generate_key():
#         """ generates a pseudo random code using os.urandom and binascii.hexlify """
#         return get_token_generator().generate_token()
#
#     user = models.ForeignKey(
#         User,
#         related_name='confirm_email_tokens',
#         on_delete=models.CASCADE,
#         verbose_name=_("The User which is associated to this password reset token")
#     )
#
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=_("When was this token generated")
#     )
#
#     # Key field, though it is not the primary key of the model
#     key = models.CharField(
#         _("Key"),
#         max_length=64,
#         db_index=True,
#         unique=True
#     )
#
#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(ConfirmEmailToken, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return "Password reset token for user {user}".format(user=self.user)
