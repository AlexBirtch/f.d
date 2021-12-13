from rest_framework import permissions

'''Проверка прав доступа / Доступно только для представителей магазинов'''
class IsShop(permissions.BasePermission):
    message = 'Данный функционал доступен только представителям магазинов.'

    def has_permission(self, request, view):
        return request.user.type == 'shop'


class IsShopOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj.user == request.user
