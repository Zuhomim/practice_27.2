from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserDestroyAPIView, UserUpdateAPIView, UserRetrieveAPIView, \
    UserCreateAPIView, UserListAPIView, PaymentCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('retrieve/<int:pk>', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('update/<int:pk>', UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/<int:pk>', UserDestroyAPIView.as_view(), name='user_delete'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
]
