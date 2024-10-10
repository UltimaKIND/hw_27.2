from django.core.management import BaseCommand

from materials.models import Course
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user_email = input("user_email: ")
        user = User.objects.all().filter(email=user_email).first()
        selected_lesson = input("title: ")
        selected_course = input("title: ")
        payment_amount = input("payment_amount: ")
        payment = input("наличные или перевод на счет")
        if selected_lesson:
            Payment.objects.create(
                user=user,
                lesson=selected_lesson,
                payment_amount=payment_amount,
                payment=payment,
            )
        elif selected_course:
            Payment.objects.create(
                user=user,
                course=selected_course,
                payment_amount=payment_amount,
                payment=payment,
            )
