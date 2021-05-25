from django.contrib import admin
from django.urls import path, include

from accounts.views import profileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('auth/', include('accounts.urls')),
    path('accounts/profile/', profileView, name='profile'),

]
