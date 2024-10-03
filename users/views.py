from rest_framework.viewsets import ModelViewSet  # type: ignore

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    контроллер CRUD пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
