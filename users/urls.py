from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentCreateAPIView,
)

from .views import PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("list/", UserListAPIView.as_view(), name="users_list"),
    path("view/<int:pk>/", UserRetrieveAPIView.as_view(), name="users_detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="users_update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="users_delete"),
    path("payment/", PaymentCreateAPIView.as_view(), name="payment"),
]
urlpatterns += router.urls
