from django.urls import path
from rest_framework.routers import SimpleRouter  # type: ignore
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import PaymentViewSet, SubscriptionAPIView, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"users", UserViewSet, basename="users")


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("subscribe/", SubscriptionAPIView.as_view(), name="subscribe"),
] + router.urls
