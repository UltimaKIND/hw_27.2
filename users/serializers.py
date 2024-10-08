from rest_framework.serializers import ModelSerializer  # type: ignore

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """
    сериализатор модели пользователя
    """

    payments = PaymentSerializer(source="payment_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class OtherUserSerializer(ModelSerializer):
    """
    сериализатор модели пользователя
    """

    class Meta:
        model = User
        exclude = ("password", "last_name")
