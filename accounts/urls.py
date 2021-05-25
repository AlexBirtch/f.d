from django.urls import path, include
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from accounts.views import RestrictedApiView, RegistrationView, ContactView

# from orders.views import registerView

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),  # /auth/token/login/ to get token
    path('', include('rest_framework.urls')),
    path('reg/', RegistrationView.as_view(), name='register'), # /auth/reg/ instead of: /auth/users/ to register a new user
    path('password_reset', reset_password_request_token, name='password-reset'),
    path('password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    path('restricted/', RestrictedApiView.as_view()),
    path('contact/', ContactView.as_view()),

]
