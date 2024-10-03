from rest_framework import serializers  # type: ignore

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    сериализатор модели пользователя
    """

    class Meta:
        model = User
        fields = "__all__"
