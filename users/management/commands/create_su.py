from django.core.management import BaseCommand

from users.models import User


# команда для создания суперпользователя
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(email="admin@sky.pro")
        user.set_password("123qwe456rty")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
