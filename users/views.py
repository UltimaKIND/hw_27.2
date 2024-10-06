from rest_framework import filters
from rest_framework.viewsets import ModelViewSet  # type: ignore

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment']
    ordering_fields = ['payment_date',]



class UserViewSet(ModelViewSet):
    """
    контроллер CRUD пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
