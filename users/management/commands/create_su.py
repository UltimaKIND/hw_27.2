from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user_email = input("user_email: ")
        user = User.objects.create(email=user_email)
        password = input("password: ")
        user.set_password(password)
        if input("is_active: "):
            user.is_active = True
        if input("is_staff: "):
            user.is_staff = True
        if input("is_superuser: "):
            user.is_superuser = True
        user.save()
