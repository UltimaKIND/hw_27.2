from rest_framework.serializers import ModelSerializer  # type: ignore

from users.models import User, Payment

class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(ModelSerializer):
    """
    сериализатор модели пользователя
    """
    payments = PaymentSerializer(source='payment_set',many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"

