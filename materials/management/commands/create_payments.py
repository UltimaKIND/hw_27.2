from users.models import User
from materials.models import Course, Payment
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.all().filter(email='test_user@sky.pro').first()
        course = Course.objects.all().filter(title='python').first()
        Payment.objects.create(user=user, course=course, payment_amount=10000.00, payment='наличные')